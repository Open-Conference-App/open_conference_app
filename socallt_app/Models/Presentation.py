from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db
from socallt_app.config import sensitive
from socallt_app.Models.Member import member_presentations
from socallt_app.Models.Conference import Conference
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
sens = sensitive.Sens()

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
		self.conference_id = present_info['conference_id']
		##Presenters should be added in the controller
		scopes = ['https://www.googleapis.com/auth/drive']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(sens.google_drive_key, scopes=scopes)
		drive = build('drive', 'v3', credentials=credentials)

		#Check for year folder
		#	Create it if it doesn't exist
		#Create a folder for the presentation (using presentation title)
		#save folder id and place files in the folder if there are any
		conference = Conference.query.get(present_info['conference_id'])
		folder = drive.files().list(q="name="+conference['year']+", mimeType='application/vnd.google-apps.folder'")
		if len(folder['files']) == 0:
			folder_params = {
				'mimeType': "application/vnd.google-apps.folder",
				'name': conference['year']
			}
			drive.files().create(body=folder_params)
			self.files_url = present_info['files_url']
