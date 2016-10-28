
from flask import render_template, session
from OCAPP import app
from OCAPP.config.sensitive import Sens
sens = Sens()
import stripe
stripe.api_key = sens.stripe_secret_key
from OCAPP.Models import Conference, State, Institution

@app.route('/')
def load_forms():
	data = {
		'conference': Conference.get_next(),
		'states': State.index(),
		'institutions': Institution.index()
	}
	return render_template('index.html', data=data)

#create a new conference(to be done through admin dashboard only via ajax call)
@app.route('/conferences', methods=['POST'])
def create_conference():

	return redirect('/') #need to replace redirect with admin dashboard url

#handle all RESTful routes to '/conference/<conference_id'
@app.route('/conferences/<conference_id>', methods=['GET','DELETE','PUT'])
def handle_conference(conference_id):
	#show next conference registration page, even if using a past conference idnumber or a non-int type
	if request.method == 'GET':
		new_conference = Conferences.get_next()
		#if the parameter in uri is not a number or not the latest id, go to the latest
		if not isinstance(conference_id, (int, long)) or conference_id != new_conference.id:
			return redirect('/conferences/',new_conference.id)
		else:
			session['csrf_token'] = sens.gen_csrf_token()
			return render_template('index.html', conference={'id':conference_id, 'year': new_conference.id})

	#delete a conference(to be done through admin dashboard only as an ajax call)
	if request.method == 'DELETE':
		return json.dumps({'result': Conferences.destroy(conference_id)})
	#update conference information(to be done through admin dashboard only as an ajax call)
	if request.method =='PUT':
		conference = Conferences.get_by_id(conference_id)
		changed_conference = Conference.update(conference, request.form['conference'])
		return json.dumps({'conference':changed_conference})

#pay for conference attendance/membership fees(which are one and the same, user must already exist)
@app.route('/conferences/<conference_id>/members/<member_id>', methods=['POST'])
def pay(conference_id, member_id):
	if '_id' not in session or 'csrf_token' not in request.form:
		return json.dumps({})
	elif request.form['csrf_token'] != session['csrf_token']:
		payment_data = {
			'token': request.form['token']
			#need to link data to data found in form
		}
		return	
