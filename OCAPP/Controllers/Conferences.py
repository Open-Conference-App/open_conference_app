from flask import render_template, session, request, redirect, flash 

from OCAPP import app,savepoint, rollback, csrf #,sentry

from OCAPP.config.sensitive import Sens
sens = Sens()
import stripe
stripe.api_key = sens.stripe_secret_key
from OCAPP.Models import Address, Conference, Member, State, Institution, Presentation
from OCAPP.Controllers import Mail
import json


@app.route('/')
def load_forms():
	data = {
		'conf': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index()
	}
	return render_template('index.html', data=data)

@app.route('/conferences', methods=['GET'])
def load_member_conferences():
	if not session['admin']:
		return redirect('/')
	confs = Conference.index();
	return render_template('dashboard/admin/conferences.html', confs=confs)

#create a new conference(to be done through admin dashboard only via ajax call)
@app.route('/conferences', methods=['POST'])
def create_conference():

	return redirect('/') #need to replace redirect with admin dashboard url

#handle all RESTful routes to '/conferences/<conference_id'
@app.route('/conferences/<int:conference_id>', methods=['GET','DELETE','PUT'])
def handle_conference(conference_id):
	print request
	#show next conference registration page, even if using a past conference idnumber or a non-int type
	if request.method == 'GET':
		next_conference = Conference.get_next()
		#if the parameter in uri is not a number or not the latest id, go to the latest
		if conference_id != next_conference.id:
			#need to render template showign that this conference is no longer open for registrations/proposals/ etc
			return redirect('/conferences/' + str(next_conference.id))
		else:
			data = {
				'conf': next_conference,
				'states': State.index(),
				'institutions': Institution.index()
			}
			return render_template('index.html', data=data)

	#delete a conference(to be done through admin dashboard only as an ajax call, to have this method, include a hidden form input with the name of '_method'
	# a value of 'DELETE')
	if request.method == 'DELETE':
		return json.dumps({'result': Conference.destroy(conference_id)})
	#update conference information(to be done through admin dashboard only as an ajax call)
	if request.method =='PUT':
		conference = Conferences.get_by_id(conference_id)
		changed_conference = Conference.update(conference, request.form['conference']) #need to process errors and add those to the dictionary.
		return json.dumps({'conference':changed_conference})


@app.route('/conferences/<int:conference_id>/prices', methods=['GET'])
def get_prices(conference_id):
	return json.dumps(Conference.get_prices(conference_id))

#register user for the conference
@app.route('/conferences/<int:conference_id>/register', methods=['POST'])
def register_user(conference_id):
	savepoint()
	addy_data = Address.create({
		'street1': request.form['street1'],
		'street2': request.form['street2'],
		'city': request.form['city'],
		'state_id': request.form['state'],
		'zip': request.form['zip'] })

	if(addy_data['all_valid']):
		data = Member.create({
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'type': request.form['regis_type'],
			'address_id': addy_data['validated_data']['id']
			})
	else:
		rollback()
		for field, errors in addy_data['errors'].items():
			for error in errors:
				flash(error, field)
		return redirect('/')

	if (data['all_valid']):
		member = Member.get_by_id(data['validated_data']['id'])
		if request.form['institution']=='other':
			inst = Institution.get(Institution.create({'name': request.form['inst-name']})['validated_data']['id'])
		else:
			inst = Institution.get(request.form['institution'])
		Member.addInst(member, inst)
		addy = Address.get(addy_data['validated_data'])
		Member.address(member,addy)
		conf_data = {
			"gluten_free": True if "gluten" in request.form else False,
			"food_pref": request.form['lunch'], 
			"days": request.form['regis_len'],
		}
		conf = Conference.register(conference_id, member,conf_data)
	else:
		rollback()
		for field, errors in data['errors'].items():
			for error in errors:
				print error
				print field
				flash(error, field)
		return redirect('/')
	if request.form['pay'] == 'check_PO':
		return render_template('confirmation.html')
	if request.form['pay'] == 'credit_debit':
		member_data = {
			'id': member.id,
			'first_name': member.first_name,
			'last_name': member.last_name,
			'email': member.email
			}
		#FIGURING OUT HOW MUCH TO CHARGE TO CREDIT CARD TRANSACTION
		conf = Conference.get_by_id(conf.id)
		days = request.form['regis_len']
		if days == 'friday' or days == 'saturday':
			day_divisor = 2
		else:
			day_divisor = 1
		member_type = member.type   
		if member_type == "Professional":
			member_type_cost = conf.prof_cost
		elif member_type == "Vendor":
			member_type_cost = conf.vend_cost
		else:
			member_type_cost = conf.stud_cost

		member_cost = member_type_cost/day_divisor

		#send success email message

		data = {
		'conf': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index(),
		'member': member
		}
		email_data = {
		"toAddy": member.email,
		"subject": "SOCALLT " + conf.year + " Registration",
		"plain_message":  "You have successfully registered and paid for SOCALLT " + conf.year + ".  We look forward to seeing you at " + conf.institution.name + ". Thank you!",
		"template": "register-mail.html",
		"data": {"data": data}
		}


		Mail.send(email_data)

		return render_template('credit_card.html', member=member_data, conf_id=conf.id, member_cost = member_cost)
	#send data by calling functions from imported files and sending it the request.form by using request.form.copy()



# # TEST ROUTE FOR RENDERING CREDIT CARD INFORMATION CHETAN 12/20/16
# @app.route('/creditcard')
# def cctest():
# 	member = {"id": 1}
# 	return render_template('credit_card.html', member=member, conf_id = 1, member_cost=30)


#pay for conference attendance/membership fees(which are one and the same, user must already exist)
@app.route('/conferences/<int:conference_id>/members/<int:member_id>', methods=['POST'])
def pay(conference_id, member_id):
	if 'id' not in session:
		return redirect('/')
	else:
		resp_object = {
			'successful': False,
			'errors': []
		}
		##validate registration prior to making payment
		memb = Member.get_by_id(member_id)
		#FAILS ON MEMB IN CONF.MEMBERS SO PUT IN 1>0 TO ALLOW IT TO PASS
		if memb in Conference.members(conference_id):
			try:
				stripe_charge = stripe.Charge.create(
					amount= int(request.form['member_cost'])*100,
					currency='usd',
					source=request.form['token'],
					description=memb.first_name + ' ' + memb.last_name + ': ' + conf.year,
					receipt_email=memb.email
					)
				active = Member.activate(memb.id)
				resp_object['successful'] = active
				Conference.set_transaction(conf.id, member_id, stripe_charge["id"]) 
			except stripe.error.CardError as e:
				resp_object['errors'].append('There was a problem charging the card you submitted.')
				body = e.json_body
				err = body['error']
				for var in err:
					resp_object['error'].append(var)
				# sentry.captureException()
			except Exception as e:
				pass
				# sentry.captureException()
		return json.dumps(resp_object)


@app.route('/conferences/<int:conference_id>/confirmation')
def confirm(conference_id):
	return render_template('confirmation.html')


@csrf.exempt
@app.route('/conferences/<int:conference_id>/proposals', methods=['POST'])
def submit_proposal(conference_id):
	savepoint()
	conf = Conference.get_by_id(conference_id)
	if not conf:
		flash('The conference indicated does not exist.')
		return redirect('/conferences/' + str(conference_id) + '/proposals')
	# print request.body
	presenters = {}
	count = 0
	for idx in range(1,4):
		fname = 'p' + str(idx) + '_f_name'
		if len(request.form[fname]) > 0:
			count += 1
		else:
			break
		lname = 'p' + str(idx) + '_l_name'
		email = 'p' + str(idx) + '_email'
		inst = 'p' + str(idx) + '_inst'
		print request.form
		mem = Member.get_by_email(request.form[email])
		is_member = False
		if mem:
			is_member = True
		presenters['Presenter' + str(idx)] = {
			'fname': request.form[fname],
			'lname': request.form[lname],
			'email': request.form[email],
			'inst': request.form[inst],
			'is_member': is_member
		}

	if count == 0:
		flash('You must supply information for at least one presenter.')
		return redirect('/conferences/' + conference_id + '/proposals')

	presenters['num'] = count
	pres = Presentation.create({
		"title": request.form["title"],
		"summary": request.form["summary"],
		"conference_id": conference_id,
		"type_id": request.form['type'],
		"preferred_time": request.form['preferred_time']
	})

	if not pres['all_valid']:
		for field, errors in pres['errors'].items():
			for error in errors:
				flash(error, field)
		return redirect('/conferences/' + str(conference_id) + '/proposals')
	
	if not Presentation.add_presenters(pres['validated_data']['id'], presenters):
		return redirect('/conferences/' + str(conference_id) + '/proposals')

	for key, presenter in presenters.items():
		if key != 'num':
			#send success email message

			data = {
			'conf': Conference.get_next(),
			'states': State.index(),
			'institutions': Institution.index(),
			'member': presenter
			}
			email_data = {
			"toAddy": presenter['email'],
			"subject": "SOCALLT " + conf.year + " Proposal Submission",
			"plain_message":  'Your presentation proposal has been recieved for SOCALLT ' + conf.year + '.  We will contact you when a decision has been made for your proposal.',
			"template": "proposal-submission.html",
			"data": {"data": data}
			}

			if not presenter['is_member']:
				email_data['plain_message'] += ' You may regsiter and pay for the conference at that time.'
			email_data['plain_message'] += ' Thank you.'

			Mail.send(email_data)
	return redirect('/conferences/' + str(conference_id) + '/proposals/success')


























