# from config import Members
from socallt_app import app
from flask import Flask, session, Session, url_for, request, render_template, redirect, flash
from socallt_app.Models.Member import Member
from socallt_app.Models.Conferences import Conferences
from socallt_app.Models.State import State

@app.route('conferences/<conference_year>')
def show_conference(conference_year):
	##what if an id is given that isn't valid?
	if not isinstance(conference_year, (int, long)):
		conference_year = Conferences.get_next_conference()
	conference_year = Conferences.get_conference_by_year(conference_year)
	return render_template('index.html', conference=conference)

@app.route('conferences/<conference_id>/register')
def new_attendee(conference_id):
	return render_template('register.html')

@app.route('session/create', methods=['POST'])
def login():
	form_data = {
		'email': request.form['email'],
		'password': request.form['password']
	}
	logged_in = logReg.login(form_data)

	if logged_in:
		return redirect('/dashboard')
	else:
		flash('The username and/or password you supplied do not match our records.', 'loginErr')
		return redirect('/')


@app.route('/members/create', methods=['POST'])
def create():
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
	if result == True:
		return redirect('/dashboard')
	else:
		return redirect('/')

@app.route('members/dashboard')
def load_dashboard():
	if '_id' in session:
		return render_template('dashboard.html')
	else:
		return redirect('/')



# @app.route('/<conference_id>/')
# def show_conference()
