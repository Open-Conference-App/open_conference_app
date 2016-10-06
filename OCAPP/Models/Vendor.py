from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from OCAPP import app, db
from OCAPP.Models.Conference import vendor_conferences

class Vendor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), unique=True)
	address_id = db.relationship(db.Integer, db.ForeignKey('address.id'))
	contact_name = db.Column(db.String(255))
	conferences = db.relationship('Conference', secondary=vendor_conferences, backref=db.backref('vendors', lazy='dynamic'))
