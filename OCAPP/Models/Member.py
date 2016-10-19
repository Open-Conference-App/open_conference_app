from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app

from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()
engine = create_engine(sens.db_path)
# Base.metadata.create_all(engine)

from OCAPP.Models.Conference import member_conferences
from OCAPP.Models.Presentation import member_presentations

class Member(Base):
	__tablename__ = 'members'
	id = Column(INTEGER(11), primary_key=True)
	first_name = Column(VARCHAR(255))
	last_name = Column(VARCHAR(255))
	address_id = Column(INTEGER(11), ForeignKey('addresses.id'))
	email = Column(VARCHAR(255), unique=True)
	password = Column(VARCHAR(255))
	pw_salt = Column(VARCHAR(255))
	officer = Column(BOOLEAN())
	member_type = Column(VARCHAR(12))
	active = Column(BOOLEAN())
	institution_id = Column(INTEGER(11), ForeignKey('institutions.id'))
	presentations = relationship('Presentation', secondary=member_presentations, back_populates='presenters')
	conferences = relationship('Conference', secondary=member_conferences, backref=backref('conf_members', lazy='dynamic'))
	created_at = Column(DATETIME())
	updated_at = Column(DATETIME())


	def __init__(self, member_data):
		self.first_name = member_data['first_name']
		self.last_name = member_data['last_name']
		self.email = member_data['email']
		self.password = member_data['password']
		self.pw_salt = member_data['pw_salt']
		self.created_at = datetime.now()
		self.updated_at = datetime.now()
		if 'officer' in member_data: self.officer = True
		else: self.officer = False
		self.active = False
		self.institution_id = member_data['institution_id']

	def __repr__(self):
		return '<Member(id=%r,email=%r>' % (self.id, self.email)



