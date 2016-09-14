from config import logReg
from socallt_app import app
from flask import Flask, session, Session, url_for, request, render_template, redirect, flash

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
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


@app.route('/register', methods=['POST'])
def register():
	form_data = {
		'username': request.form['username'],
		'email':request.form['email'],
		'password': request.form['password'],
		'confirm_password': request.form['confirm_password']
	}
	result = logReg.register(form_data)
	print 'Made it back!'
	if result == True:
		return redirect('/dashboard')
	else:
		return redirect('/')

@app.route('/dashboard')
def load_dashboard():
	if '_id' in session:
		return render_template('dashboard.html')
	else:
		return redirect('/')

@app.route('/<conference_id>')
def show_conference(conference_id):
	return ''
@app.route('/<conference_id>/register')
def new_attendee(conference_id):
	return render_template('register.html', conference_year=year)

# @app.route('/<conference_id>/')
# def show_conference()
