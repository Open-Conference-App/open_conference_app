from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db
from Conference import member_conferences

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	address_id = db.relationship(db.Integer, db.ForeignKey('address.id'))
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	pw_salt = db.Column(db.String(255))
	officer = db.Column(db.Boolean)
	member_type = db.Column(db.String(12))
	active = db.Column(db.Boolean)
	institution_id = db.relationship(db.Integer, db.ForeignKey('institution.id'))
	conferences = db.relationship('Conference', secondary=member_conferences, backref=db.backref('conf_members', lazy='dynamic'))
	created_at = db.Column(db.DateTime())
	updated_at = db.Column(db.DateTime())


	def __init__(self, member_data):
		self.first_name = member_data['first_name']
		self.last_name = member_data['last_name']
		self.email = member_data['email']
		self.password = member_data['password']
		self.pw_salt = member_data['pw_salt']
		self.created_at = datetime.now()
		self.updated_at = datetime.now()
		if 'officer' in member_data: self.officer = True
		else: self.officer = False
		self.active = False
		self.institution_id = member_data['institution_id']

	def __repr__(self):
		return '<Member %r>' % self.email


