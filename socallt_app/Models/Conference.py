from flask import Flask
import imp, re, hashlib, binascii, os
from socallt_app import app, db

class Conference(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	institution_id = db.Column(db.Integer, db.ForeignKey('member.id'))
	members = db.relationship('Member', backref='conference', lazy='dynamic')
