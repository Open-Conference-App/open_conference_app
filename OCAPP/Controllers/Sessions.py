from flask import session, flash
from OCAPP.Models.Member import Member
from OCAPP import app, db

def create(post_info):
	member = Member.query.filter_by(email=post_info['email']).first()
	is_valid = True
	if not user:
		return False
	if user.password != hashlib.sha256(user_data['password'] + user.pw_salt).hexdigest():
		is_valid = False
	if is_valid:
		session['_id'] = user.id
		session['username'] = user.username
	return is_valid

def delete():
	return