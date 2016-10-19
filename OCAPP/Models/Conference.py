from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME
from OCAPP import app
from apiclient.discovery import build

from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()
engine = create_engine(sens.db_path)

member_conferences = Table('member_conferences', Base.metadata,
	Column('member_id', INTEGER(11), ForeignKey('members.id')), 
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

vendor_conferences = Table('vendor_conferences', Base.metadata,
	Column('vendor_id', INTEGER(11), ForeignKey('vendors.id')),
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

presenter_conferences = Table('presenter_conferences', Base.metadata,
	Column('presenter_id', INTEGER(11), ForeignKey('members.id')), 
	Column('conference_id', INTEGER(11), ForeignKey('conferences.id'))
)

class Conference(Base):
	__tablename__ = 'conferences'
	id = Column(INTEGER(11), primary_key=True)
	year = Column(VARCHAR(4), unique=True)
	institution_id = Column(INTEGER(11), ForeignKey('institutions.id'))
	members = relationship('Member', secondary=member_conferences, backref=backref('conferences', lazy='dynamic'))
	vendors = relationship('Vendor', secondary=vendor_conferences, backref=backref('conferences', lazy='dynamic'))
	prof_cost = Column(INTEGER(3))
	stud_cost = Column(INTEGER(3))
	vend_cost = Column(INTEGER(3))
	date = Column(DATETIME())
	folder_id = Column(VARCHAR(255))
	created_at = Column(DATETIME())
	updated_at = Column(DATETIME())

	def __repr__(self):
		return "<Conference(year=%s)>" % self.year

	def __init__(self, conference_data):
		self.institution_id = conference_data['institution_id']
		self.year = conference_data['year']
		self.prof_cost = conference_data['prof_cost']
		self.stud_cost = conference_data['stud_cost']
		self.vend_cost = conference_data['vend_cost']
		self.date = conference_data['date']
		
		folder_metadata = {
			'name': conference_data['year'],
			'mimeType': 'application/vnd.google-apps.folder',


		}
		self.created_at = datetime.now()
		self.updated_at = datetime.now()


