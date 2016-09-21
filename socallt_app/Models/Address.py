from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db

class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	street1 = db.Column(db.String(255))
	street2 = db.Column(db.String(255))
	city = db.Column(db.String(255))
	state_id = db.relationship(db.Integer, db.ForeignKey('state.id'))
	zip = db.Column(db.String(5))

	def __init__(self, address_data):
		self.street1 = address_data['street1']
		self.street2 = address_data['street2']
		self.city = address_data['city']
		self.state_id = address_data['state_id']
		self.zip = address_data['zip']
