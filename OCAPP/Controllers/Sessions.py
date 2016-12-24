from flask import session, flash, request, redirect
from OCAPP.Models import Member
from OCAPP import app, sentry
import hashlib

@app.route('/sessions', methods=['POST'])
def login():
	member = Member.get_by_email(request.form['email'])
	valid = True
	if not member:
		valid = False
	if member:
		if member.password != hashlib.sha256(member.pw_salt + request.form['password'] ).hexdigest():
			valid = False
	if not valid:
		flash('The email address and/or password you supplied do not match our records.', 'loginErr')
		return redirect('/')

	else:
		session['id'] = member.id
		session['email'] = member.email
		session['first_name'] = member.first_name
		if member.officer:
			session['admin'] = True
		sentry.user_context({
			'email': member.email,
			'institution': member.institution.name
			})
		return redirect('/members/dashboard')


def create(cred):
	is_valid = True
	if not member:
		return False
	if member.password != hashlib.sha256(cred['password'] + user.pw_salt).hexdigest():
		is_valid = False
	if is_valid:
		session['_id'] = user.id
		session['username'] = user.username
	if member.officer:
		session['admin'] = True
	return is_valid

def delete():
	session.clear()
	return