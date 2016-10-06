from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from OCAPP import app, db

class Institution(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), unique=True)
	contact_name = db.Column(db.String(255))
	address_id = db.relationship(db.Integer, db.ForeignKey('address.id'))
	members = db.relationship('Member', backref='institution', lazy='dynamic')
	created_at = db.Column(db.DateTime())
	updated_at = db.Column(db.DateTime())

	def __init__(self, inst_data):
		self.name = inst_data['name']
		self.contact = inst_data['contact']
		self.created_at = datetime.now()
		self.updated_at = datetime.now()
