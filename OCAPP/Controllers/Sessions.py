from flask import session, flash
from OCAPP.Models.Member import Member
from OCAPP import app

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


def create(cred):
	member = Member.query.get(cred['id'])
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