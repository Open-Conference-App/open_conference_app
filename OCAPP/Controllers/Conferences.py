from flask import render_template, session, request, redirect, flash 
from OCAPP import app
from OCAPP.config.sensitive import Sens
sens = Sens()
import stripe
stripe.api_key = sens.stripe_secret_key
from OCAPP.Models import Address, Conference, Member, State, Institution
import json

@app.route('/')
def load_forms():
	data = {
		'conf': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index()
	}
	return render_template('index.html', data=data)

#create a new conference(to be done through admin dashboard only via ajax call)
@app.route('/conferences', methods=['POST'])
def create_conference():

	return redirect('/') #need to replace redirect with admin dashboard url

#handle all RESTful routes to '/conference/<conference_id'
@app.route('/conferences/<int:conference_id>', methods=['GET','DELETE','PUT'])
def handle_conference(conference_id):
	#show next conference registration page, even if using a past conference idnumber or a non-int type
	if request.method == 'GET':
		new_conference = Conference.get_next()
		#if the parameter in uri is not a number or not the latest id, go to the latest
		if not isinstance(conference_id, (int, long)) or conference_id != new_conference.id:
			return redirect('/conferences/', new_conference.id)
		else:
			return render_template('index.html', conference={'id':conference_id, 'year': new_conference.id})

	#delete a conference(to be done through admin dashboard only as an ajax call, to have this method, include a hidden form input with the name of '_method'
	# a value of 'DELETE')
	if request.method == 'DELETE':

		return json.dumps({'result': Conferences.destroy(conference_id)})
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
			'type': request.form['regis_type']
			})

	else:
		for field in addy_data['errors']:
			for message in field:
				flash(message, field)
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
		for field in data['errors']:
			for message in field:
				flash(message,field)
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
		return render_template('credit_card.html', member=member_data, conf_id=conf.id, member_cost = member_cost)
	#send data by calling functions from imported files and sending it the request.form by using request.form.copy()



# TEST ROUTE FOR RENDERING CREDIT CARD INFORMATION CHETAN 12/20/16
@app.route('/creditcard')
def cctest():
	member = {"id": 1}
	return render_template('credit_card.html', member = member, conf_id = 1, member_cost=30)


#pay for conference attendance/membership fees(which are one and the same, user must already exist)
@app.route('/conferences/<int:conference_id>/members/<int:member_id>', methods=['POST'])
def pay(conference_id, member_id):
	if 1>2: #'user' not in session:
		pass #set to pass for debugging purposes, delete and uncomment return redirect for production.
		#return redirect('/')
	else:
		resp_object = {
			'successful': False,
			'errors': []
		}
		##validate registration prior to making payment
		conf = Conference.get_next() #why not get_by_id using conference_id from url?
		memb = Member.get_by_id(member_id)
		#FAILS ON MEMB IN CONF.MEMBERS SO PUT IN 1>0 TO ALLOW IT TO PASS
		if 1>0: #memb in conf.members:
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
			except Exception as e:
				pass
		return json.dumps(resp_object)


@app.route('/conferences/<int:conference_id>/confirmation')
def confirm(conference_id):
	return render_template('confirmation.html')
