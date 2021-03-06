from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, Base, BaseChanges
from apiclient.discovery import build
from OCAPP.config import sensitive
sens = sensitive.Sens()

#join table for members<>conferences
class Registration(BaseChanges, Base):
	__tablename__ = 'registrations'
	id = Column(INTEGER(11), primary_key=True, autoincrement=True)
	member_id = Column(INTEGER(11), ForeignKey('members.id'), primary_key=True)
	conference_id = Column(INTEGER(11), ForeignKey('conferences.id'), primary_key=True)
	food_pref = Column(VARCHAR(255))
	gluten_free = Column(BOOLEAN())
	days = Column(VARCHAR(255))
	type = Column(VARCHAR(255))
	member_paid = Column(BOOLEAN())
	transaction_id = Column(VARCHAR(255))
	member = relationship('Member', back_populates='registrations')
	conference = relationship('Conference', back_populates='registrations')

	def __init__(self, data):
		self.food_pref = data['food_pref']
		self.gluten_free = data['gluten_free']
		self.member_paid = False
	
	def __repr__(self):
		return "<Registration(id=%s, member=%s, conference=%s)>" % (self.id, self.member_id, self.conference_id)


#join table for vendors
vendor_conferences = Table('vendor_conferences', Base.metadata,
	Column('vendor_id', INTEGER(11), ForeignKey('vendors.id')),
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

#join table for presenters
presenter_conferences = Table('presenter_conferences', Base.metadata,
	Column('presenter_id', INTEGER(11), ForeignKey('members.id')), 
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

class Conference(BaseChanges, Base):
	__tablename__ = 'conferences'
	id = Column(INTEGER(11), primary_key=True)
	title = Column(VARCHAR(255))
	year = Column(VARCHAR(4), unique=True)
	institution_id = Column(INTEGER(11), ForeignKey('institutions.id'))
	institution = relationship('Institution')
	registrations = relationship('Registration', back_populates='conference')
	vendors = relationship('Vendor', secondary=vendor_conferences, backref=backref('vendor_conferences', lazy='dynamic'))
	host_id = Column(INTEGER(11), ForeignKey('members.id'))
	host = relationship('Member')
	presentations = relationship('Presentation', back_populates='conference')
	prof_cost = Column(INTEGER(3)) # all costs are stored in cents for stripe purposes
	stud_cost = Column(INTEGER(3))
	vend_cost = Column(INTEGER(3))
	proposal_deadline = Column(DATETIME())
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
		self.proposal_deadline = conference_data['proposal_deadline']
		self.end_date = conference_data['end_date']
		self.title = conference_data['title']
		 #need to pass date object, but first I need format of date object coming from client-side
		
		# folder_metadata = {
		# 	'name': conference_data['year'],
		# 	'mimeType': 'application/vnd.google-apps.folder',


		# }
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()

	# def members(self):
	# 	members = []
	# 	for registration in self.members:
	# 		memb = Member.get_by_id(registration.member_id)
	# 		if memb:
	# 			members.append(memb)
	# 	return members








