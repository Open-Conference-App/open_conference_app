import binascii, os, re, hashlib
from OCAPP.config.sensitive import Sens
from flask import session, flash
from flask_sqlalchemy import SQLAlchemy
sens = Sens()
from OCAPP.Models.Member import Member
from OCAPP import app, db
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
		if Member.query.filter_by(email=fields['email']).first():
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

def activate(id):	
	member = Member.query.get(id)
	if member:
		active = True
	else:
		active = False
	member = Member.query.get(id)
	member.active = active
	db.session.commit()
	return member.active

def deactivate(id):
	member = Member.query.get(id)
	if member:
		active = False
	else:
		active = True
	member = Member.query.get(id)
	member.active = active
	db.session.commit()
	return member.active

def toggle_officer(member_id, make_officer):
	member = Member.query.get(member_id)
	member.officer = True if make_officer else False
	db.session.commit()
	return member_id

def update(member_data):
	##assumes to have had all other table data removed before receipt
	member = Member.query.get(member_data)
	for k,v in member_data:
		if member[k] != v:
			member[k] = v
	return member

def index():
	return Member.query.all()

def get_by_email(email_add):
	return Member.query.filter_by(email=email_add).first()



	
