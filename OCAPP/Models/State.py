from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from OCAPP import app, db

class State(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	abbrev = db.Column(db.String(2))


	def __init__(self, abbrev):
		self.abbrev = abbrev