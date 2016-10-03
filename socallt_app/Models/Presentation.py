from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from socallt_app import app, db
from socallt_app.config import sensitive
from socallt_app.Models.Member import member_presentations
from socallt_app.Models.Conference import Conference
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
sens = sensitive.Sens()
scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(sens.google_drive_key, scopes=scopes)
drive = build('drive', 'v3', credentials=credentials)

member_presentations = db.Table('member_presentations', 
	db.Column('presenter_id', db.Integer, db.ForeignKey('member.id')), 
	db.Column('presentation_id', db.Integer, db.ForeignKey('presentation.id'))
)

class Presentation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), unique=True)
	summary = db.Column(db.Text())
	files_url = db.Column(db.Text()) ##trying to utilize Google Drive for file upload
	approved = db.Column(db.Boolean)
	presenters = db.relationship('Member', secondary=member_presentations, back_populates='presentations')
	conference_id = db.relationship(db.Integer, db.ForeignKey('conference.id'))

	def __init__(self, present_info):
		self.title = present_info['title']
		self.summary = present_info['summary']
		self.approved = False
		self.conference_id = present_info['conference_id']
		self.add_files(present_info['files']) if 'files' in present_info else None
		self.presenters = present_info['presenters']
		##Presenters should be added in the controller

		#Check for year folder
		#	Create it if it doesn't exist
		#Create a folder for the presentation (using presentation title)
		#save folder id and place files in the folder if there are any
	def add_files(self, files):	
		conference = Conference.query.get(self.conference_id)
		#check for conference year folder, create if none
		year_folder = drive.files().list(q="name="+conference['year']+" and mimeType='application/vnd.google-apps.folder'")
		if len(year_folder['files']) == 0:
			folder_params = {
				'mimeType': "application/vnd.google-apps.folder",
				'name': conference['year'],
				'parents': sens.drive_root_folder_id
			}
			drive.files().create(body=folder_params).execute()

		#check for presentation folder, create if none
		present_folder = drive.files().list(q="name="+self.title+" and mimeType='application/vnd.google-apps.folder'")
		if len(present_folder['files']) == 0:
			folder_params = {
				'mimeType': "application/vnd.google-apps.folder",
				'name': self.title,
				'parents': year_folder['files'][0]['id']
			}
			drive.files().create(body=folder_params).execute()
		#Upload each file to the folder
		for file in files:
			file_data = {
				'name': file['name'],
				'parents': present_folder['files'][0]['id']
			}
			drive.files.create(body=file_data, media_body=file['file'])
		self.files_url = drive.files(fileId=present_folder['files'][0]['id'])['webViewLink']


