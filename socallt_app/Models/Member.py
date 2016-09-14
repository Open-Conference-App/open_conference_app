from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	pw_salt = db.Column(db.String(255))
	officer = db.Column(db.Boolean)
	active = db.Column(db.Boolean)
	created_at = db.Column(db.DateTime())
	updated_at = db.Column(db.DateTime())


	def __init__(self, first_name, last_name, email, password, pw_salt, officer):
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.password = password
		self.pw_salt = pw_salt
		self.created_at = datetime.now()
		self.upated_at = datetime.now()
		if officer self.officer = True
		else self.officer = False
		self.active = False

	def __repr__(self):
		return '<Member %r>' % self.email


