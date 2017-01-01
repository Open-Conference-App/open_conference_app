import binascii, os, re, hashlib
from OCAPP.config.sensitive import Sens
from flask import session, flash
from flask_sqlalchemy import SQLAlchemy
sens = Sens()
from OCAPP.Schema.Member import Member
from OCAPP import app, db
EMAIL_KEY = re.compile(r'^[a-zA-Z0-9\.\+_-]@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

def create(fields):
	valid_obj = db.create(Member,fields)
	return valid_obj

def activate(id):	
	member = db.query(Member).filter_by(id=id).first()
	if member:
		active = True
	else:
		active = False
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

def update(member_data):
	##assumes to have had all other table data removed before receipt
	member = Member.query.get(member_data)
	for k,v in member_data:
		if member[k] != v:
			member[k] = v
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



	
