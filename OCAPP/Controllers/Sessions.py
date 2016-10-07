from flask import session, flash
from OCAPP.Models.Member import Member
from OCAPP import app, db

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