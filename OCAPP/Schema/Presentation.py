from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN, TEXT
from OCAPP import app, db
import datetime

from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)
from OCAPP.Models.BaseChanges import BaseChanges


from OCAPP.Models.Conference import Conference
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(sens.google_drive_key, scopes=scopes)
drive = build('drive', 'v3', credentials=credentials)

member_presentations = Table('member_presentations', db.Base.metadata,
	Column('presenter_id', INTEGER(11), ForeignKey('members.id')), 
	Column('presentation_id', INTEGER(11), ForeignKey('presentations.id'))
)

class Presentation(BaseChanges, db.Base):
	__tablename__ = 'presentations'
	id = Column(INTEGER(11), primary_key=True)
	title = Column(VARCHAR(255), unique=True)
	summary = Column(TEXT())
	files_url = Column(TEXT()) ##trying to utilize Google Drive for file upload
	approved = Column(BOOLEAN())
	duration = Column(INTEGER(2)) #time in minutes
	datetime = Column(DATETIME())
	presenters = relationship('Member', secondary=member_presentations, back_populates='presentations')
	conference_id = Column(INTEGER(11), ForeignKey('conferences.id'))
	conference = relationship('Conference', back_populates='presentations', uselist=False)
	created_at = Column(DATETIME(), default=func.utc_timestamp())
	updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())

	def __init__(self, present_info):
		self.title = present_info['title']
		self.summary = present_info['summary']
		self.approved = False
		self.conference_id = present_info['conference_id']
		self.duration = present_info['duration'] #time in minutes
		self.add_files(present_info['files']) if 'files' in present_info else None
		self.presenters.append(**present_info['presenters'])
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

