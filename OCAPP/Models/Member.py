from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, db

from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)

from OCAPP.Models.Conference import member_conferences
from OCAPP.Models.Presentation import member_presentations

class Member(db.Base):
	__tablename__ = 'members'
	id = Column(INTEGER(11), primary_key=True)
	first_name = Column(VARCHAR(255))
	last_name = Column(VARCHAR(255))
	address_id = Column(INTEGER(11), ForeignKey('addresses.id'))
	address = relationship('Address', )
	email = Column(VARCHAR(255), unique=True)
	password = Column(VARCHAR(255))
	pw_salt = Column(VARCHAR(255))
	officer = Column(BOOLEAN())
	member_type = Column(VARCHAR(12))
	active = Column(BOOLEAN())
	institution_id = Column(INTEGER(11), ForeignKey('institutions.id'))
	institution = relationship('Institution', back_populates='faculty_members')
	host = Column(BOOLEAN())
	presentations = relationship('Presentation', secondary=member_presentations, back_populates='presenters')
	conferences = relationship('Conference', secondary=member_conferences, backref=backref('conf_members', lazy='dynamic'))
	created_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())
	updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())


	def __init__(self, member_data):
		self.first_name = member_data['first_name']
		self.last_name = member_data['last_name']
		self.email = member_data['email']
		self.password = member_data['password']
		self.pw_salt = member_data['pw_salt']
		self.officer = True if 'officer' in member_data else False
		self.active = False
		self.institution_id = member_data['institution_id']

	def __repr__(self):
		return '<Member(id=%r,email=%r>' % (self.id, self.email)



