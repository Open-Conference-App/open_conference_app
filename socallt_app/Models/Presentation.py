from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db
from socallt_app.Models.Member import member_presentations

class Presentation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True)
	summary = db.Column(db.Text())
	files_url = db.Column(db.Text()) ##trying to utilize Google Drive for file upload
	approved = db.Column(db.Boolean)
	presenters = db.relationship('Member', secondary=member_presentations, backref=db.backref('presentations', lazy='dynamic'))
	conference_id = db.relationship(db.Integer, db.ForeignKey('conference.id'))

	def __init__(self, present_info):
		self.title = present_info['title']
		self.summary = present_info['summary']
		self.approved = False
		##how do I save data in a join table when adding a presenter/presenters?
		member_presentations
		if 'url' in present_info:
			self.files_url = present_info['files_url']
