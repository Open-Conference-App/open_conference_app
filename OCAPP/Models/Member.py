import binascii, os, re, hashlib
from OCAPP.config.sensitive import Sens
from flask import session, flash
from flask_sqlalchemy import SQLAlchemy
sens = Sens()
from OCAPP.Schema.Member import Member
from OCAPP.Schema.PasswordReset import PasswordReset
from OCAPP import app, SQLEZ, sentry, BaseChanges
db = SQLEZ()
EMAIL_KEY = re.compile(r'^[a-zA-Z0-9\.\+_-]@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def create(fields):
	valid_obj = db.create(Member,fields)
	return valid_obj

def activate(id):
	print id	
	member = db.get(Member, id)
	if member:
		active = True
	else:
		active = False
		print member
	member.active = active
	db.session.add(member)
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

#def update(member_data):
	##assumes to have had all other table data removed before receipt
#	member = Member.query.get(member_data['id'])
#	for k,v in member_data['fields'].items():
	#	if member[k] != v:
	#	SQLEZ.BaseChanges.validate(Member, member_data 
	#		member[k] = v
	#return member
def change_password(member, new_pass):
	pass_data = BaseChanges.process_password(Member, {'password': new_pass})
	if pass_data['errors']['password']:
		return pass_data
	member.password = pass_data['hash']
	member.pw_salt = pass_data['salt']
	db.session.add(member)
	db.session.commit()
	return member
		
def index():
	return db.query(Member).order_by(Member.last_name).all()

def get_by_email(email_add):
	return db.query(Member).filter_by(email=email_add).first()

def get_by_id(id):
	return db.query(Member).filter_by(id=id).first()

def address(mem, data):
	mem.address = data
	db.session.add(mem)
	db.session.commit()
	return mem

def addInst(mem, inst):
	mem.institution = inst
	db.session.add(mem)
	db.session.commit()
	return mem

def generate_reset_hash(mem_id):
        hash = binascii.hexlify(os.urandom(32))
	pw_reset = PasswordReset({
                "id": mem_id,
        })
	db.session.add(pw_reset)
	db.session.commit()
        return pw_reset.reset_hash

def find_reset_hash(hash):
	return  db.query(PasswordReset).filter(PasswordReset.reset_hash == hash).first()
	
