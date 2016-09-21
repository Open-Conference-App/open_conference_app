import binascii, os, re, hashlib
from sensitive import Sens
from flask import session, flash
from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy
sens = Sens()
from socallt_app.Models.Member import Member
from socallt_app import app, db

EMAIL_KEY = re.compile(r'^[a-zA-Z0-9\.\+_-]@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
def create(fields):
	is_valid = True
	for k, v in fields.items():
		print v
		if not v:
			flash('All fields are required.', 'regisErr')
			return False
	if EMAIL_KEY.match(fields['email']) != None:
		is_valid = False
		flash("Email address is not formatted correctly.", 'regisErr')
	else:
		if User.query.filter_by(email=fields['email']).first():
			flash("The email address you entered is already in our system.", 'regisErr')
			is_valid = False
	if fields['password'] != fields['confirm_password']:
		flash("Passwords do not match",'regisErr')
		is_valid=False
	if not is_valid:
		return False
	else:
		fields['pw_salt'] = binascii.hexlify(os.urandom(16))
		fields['password'] = hashlib.sha256(fields['password'] + fields['pw_salt']).hexdigest()
		user_data = {
			'first_name': fields['first_name'],
			'last_name': fields['last_name'],
			'email': fields['email'],
			'password': fields['password'],
			'pw_salt': fields['pw_salt'],
			'street1': fields['street1'],
			'street2': fields['street2'],
			'city': fields['city'],
			'state': fields['state'],
			'zip': fields['zip']
		}
		user = User(**user_data)
		db.session.add(user)
		db.session.commit()
		session['_id'] = user.id
		session['username'] = user.username
	return True

def login(user_data):
	print user_data['email']
	user = User.query.filter_by(email=user_data['email']).first()
	is_valid=True
	if not user:
		return False
	if user.password != hashlib.sha256(user_data['password'] + user.pw_salt).hexdigest():
		is_valid = False
	if is_valid:
		session['_id'] = user.id
		session['username'] = user.username
	return is_valid


	
