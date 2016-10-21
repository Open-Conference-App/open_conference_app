from OCAPP.config.sensitive import Sens
sens = Sens()
from OCAPP import app
from flask import Flask, session, url_for, request, render_template, redirect, flash
from OCAPP.Models import Address, Conference, Institution, Member, Presentation, State, Vendor
from OCAPP.Controllers import Conferences, Addresses, Institutions, Members, Presentations, States, Vendors, Sessions
import stripe
stripe.api_key = sens.stripe_secret_key

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
def register_and_pay(conference_id, member_id):
	if '_id' not in session or 'csrf_token' not in request.form:
		return json.dumps({})
	elif request.form['csrf_token'] != session['csrf_token']:
		payment_data = {
			'token': request.form['token']
			#need to link data to data found in form
		}
		return	

@app.route('/sessions/', methods=['POST'])
def login():
	form_data = {
		'email': request.form['email'],
		'password': request.form['password']
	}
	member = Members.get_by_email(form_data['email'])
	if member:
		logged_in = Sessions.create(member)
	if logged_in:
		return redirect('/dashboard')
	else:
		flash('The email address and/or password you supplied do not match our records.', 'loginErr')
		return redirect('/')


#create a new member(when users regsiter for the next conference)
@app.route('/members', methods=['POST'])	
def create_memb():
	if not 'csrf_token' in session:
		return redirect('/conferences')
	#what's the route for adming dashboard??
	return redirect('/')




#creates new user in db (should be utilized if it is a new member only)
@app.route('/members/<member_id>', methods=['GET','PUT', 'DELETE'])
def handle_members(member_id):
	#show member info
	if request.method == 'GET':
		if not isinstance(conference_id, (int, long)):
			conference_id = Conferences.get_next()
		return render_template('index.html', conference={'id':conference_id})

	#delete a conference(to be done through admin dashboard only)
	if request.method == 'DELETE':
		return redirect('/')

	#update conference information(to be done through admin dashboard only)
	if request.method =='PUT':
		form_data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email':request.form['email'],
			'password': request.form['password'],
			'confirm_password': request.form['confirm_password'],
			'street1': request.form['street1'],
			'street2': request.form['street2'],
			'city': request.form['city'],
			'state': request.form['state'],
			'zip': request.form['zip']
		}

		result = Members.create(form_data)
	if result:
		form_data = {}
		if 'inst-name' in request.form:
			form_data['inst-name'] = request.form['inst-name']
			form_data['inst-state'] = request.form['inst-state']
			inst = Institutions.create(form_data)
	if result:
		return redirect('/dashboard')
	else:
		return redirect('/')

@app.route('/members/dashboard')
def load_dashboard():
	if '_id' in session:
		session['csrf_token'] = sens.gen_csrf_token()
		return render_template('dashboard.html')
	else:
		return redirect('/')

