from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, db
from apiclient.discovery import build

from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)
from OCAPP.Models.BaseChanges import BaseChanges

#join table for members<>conferences
class MemberConferences(BaseChanges, db.Base):
	__tablename__ = 'member_conferences'
	id = Column(INTEGER(11), primary_key=True, autoincrement=True)
	member_id = Column(INTEGER(11), ForeignKey('members.id'), primary_key=True)
	conference_id = Column(INTEGER(11), ForeignKey('conferences.id'), primary_key=True)
	food_pref = Column(VARCHAR(255))
	gluten_free = Column(BOOLEAN())
	days = Column(VARCHAR(255))
	member_paid = Column(BOOLEAN())
	transaction_id = Column(VARCHAR(255))
	member = relationship('Member', back_populates='conferences')
	conference = relationship('Conference', back_populates='members')

	def __init__(self, data):
		self.food_pref = data['food_pref']
		self.gluten_free = data['gluten_free']
		self.member_paid = False

	def __repr__(self):
		return "<MemberConference(id=%s, member=%s, conference=%s)>" % (self.id, self.member_id, self.conference_id)


#join table for vendors
vendor_conferences = Table('vendor_conferences', db.Base.metadata,
	Column('vendor_id', INTEGER(11), ForeignKey('vendors.id')),
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

#join table for presenters
presenter_conferences = Table('presenter_conferences', db.Base.metadata,
	Column('presenter_id', INTEGER(11), ForeignKey('members.id')), 
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

class Conference(BaseChanges, db.Base):
	__tablename__ = 'conferences'
	id = Column(INTEGER(11), primary_key=True)
	title = Column(VARCHAR(255))
	year = Column(VARCHAR(4), unique=True)
	institution_id = Column(INTEGER(11), ForeignKey('institutions.id'))
	institution = relationship('Institution')
	members = relationship('MemberConferences', back_populates='conference')
	vendors = relationship('Vendor', secondary=vendor_conferences, backref=backref('vendor_conferences', lazy='dynamic'))
	host_id = Column(INTEGER(11), ForeignKey('members.id'))
	host = relationship('Member')
	presentations = relationship('Presentation', back_populates='conference')
	prof_cost = Column(INTEGER(3)) # all costs are stored in cents for stripe purposes
	stud_cost = Column(INTEGER(3))
	vend_cost = Column(INTEGER(3))
	start_date = Column(DATETIME())
	end_date = Column(DATETIME())
	folder_id = Column(VARCHAR(255))
	created_at = Column(DATETIME(), default=func.utc_timestamp())
	updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())

	def __repr__(self):
		return "<Conference(year=%s)>" % self.year

	def __init__(self, conference_data):
		self.year = conference_data['year']
		self.prof_cost = conference_data['prof_cost']
		self.stud_cost = conference_data['stud_cost']
		self.vend_cost = conference_data['vend_cost']
		self.start_date = conference_data['start_date']
		self.end_date = conference_data['end_date']
		self.title = conference_data['title']
		 #need to pass date object, but first I need format of date object coming from client-side
		
		# folder_metadata = {
		# 	'name': conference_data['year'],
		# 	'mimeType': 'application/vnd.google-apps.folder',


		# }
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()

