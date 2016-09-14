from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db

member_conferences = db,Table('member_conferences', 
	db.Column('member_id', db.Integer, db.ForeignKey('member.id')), 
	db.Column('conference_id', db.Integer, db.ForeignKey('conference.id'))
)

vendor_conferences = db.Table('vendor_conferences',
	db.Column('vendor_id', db.Integer, db.ForeignKey('vendor.id')),
	db.Column('conference_id', db.Integer, db.ForeignKey('conference.id'))
)

class Conference(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	institution_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	members = db.relationship('Member', secondary=member_conferences, backref=db.backref('conferences', lazy='dynamic'))
	vendors = db.relationship('Vendor', secondary=vendor_conferences, backref=db.backref('vendors', lazy='dynamic'))
	cost = db.Column(db.Integer)
	date = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self, conference_data):
		self.institution_id = conference_data['institution_id']
		self.cost = conference_data['cost']
		self.date = conference_data['date']
		self.created_at = datetime.now()
		self.updated_at = datetime.now()
