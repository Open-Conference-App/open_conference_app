
from flask import render_template, session
from OCAPP import app
from OCAPP.config.sensitive import Sens
sens = Sens()
import stripe
stripe.api_key = sens.stripe_secret_key
from OCAPP.Models import Conference, State, Institution
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



#pay for conference attendance/membership fees(which are one and the same, user must already exist)
@app.route('/conferences/<conference_id>/members/<member_id>', methods=['POST'])
@sens.check_session
def pay(conference_id, member_id):
	if 'id' not in session or 'csrf_token' not in request.form:
		return redirect('/dashboard')
	elif request.form['csrf_token'] in csrf_token:
		##validate registration prior to making payment
			
		if request.form['pay'] == 'credit_debit':
			conf = Conference.get_by_id(conference_id)
			price = getattr(conf, request.form['regis_type'])
			try:
				charge = stripe.Charge.create(
					amount= price if request.form['regis_len'] == 'Entire Confernece' else price/2,
					currency='usd',
					source=request.form['stripe_token'],
					description=request.form['first_name'] + ' ' + request.form['last_name'] + ': ' + conf.year
					)
			except:
				pass
		return	
