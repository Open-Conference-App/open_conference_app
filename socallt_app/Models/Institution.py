from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db

class Institution(db.Model):
	id = db.Column(db.Integer, primary_key=True)