from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, db
from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)
from OCAPP.Models.BaseChanges import BaseChanges


# from OCAPP.Models.Conference import member_conferences
from OCAPP.Models.Presentation import member_presentations

class Member(BaseChanges,db.Base):
	__tablename__ = 'members'
	id = Column(INTEGER(11), primary_key=True)
	first_name = Column(VARCHAR(255))
	last_name = Column(VARCHAR(255))
	address_id = Column(INTEGER(11), ForeignKey('addresses.id'))
	address = relationship('Address')
	email = Column(VARCHAR(255), unique=True)
	password = Column(VARCHAR(255))
	pw_salt = Column(VARCHAR(255))
	officer = Column(BOOLEAN())
	member_type = Column(VARCHAR(20))
	active = Column(BOOLEAN())
	institution_id = Column(INTEGER(11), ForeignKey('institutions.id'))
	institution = relationship('Institution', back_populates='faculty_members')
	host = relationship('Conference', uselist=False, back_populates='host')
	presentations = relationship('Presentation', secondary=member_presentations, back_populates='presenters')
	conferences = relationship('MemberConferences', back_populates='member')
	created_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())
	updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())

	def __init__(self, member_data):
		self.first_name = member_data['first_name']
		self.last_name = member_data['last_name']
		self.address_id = member_data['address_id']
		self.email = member_data['email']
		self.pw_salt = member_data['salt']
		self.password = member_data['hash']
		self.officer = True if 'officer' in member_data else False
		self.active = False
		self.institution_id = member_data['institution_id']

	def __repr__(self):
		return '<Member(id=%r,email=%r>' % (self.id, self.email)

	#runs all validations and consolidates errors to send back to controller
	# @staticmethod
	# def validate(member_data):
	# 	try:
	# 		blanks_info = valids.check_blanks(member_data)
	# 		if not blanks_info['all_valid']:
	# 			all_valid = False
	# 			for error in blanks_info['errors']:
	# 				validations['errors'].append(error)

	# 		email_info = valids.check_email(member_data['email'])
	# 		if not email_info['all_valid']:
	# 			all_valid = False
	# 			for error in email_info['errors']:
	# 				validations['errors'].append(error)
	# 		if all_valid:
	# 			#validates and processes pw, returns salt and hash
	# 			pw_info = valids.process_password(member_data['password'])
	# 			if not pw_info['all_valid']:
	# 				all_valid = False
	# 				for error in pw_info['errors']:
	# 					validations['errors'].append(error)
	# 			else:
	# 				member_data['salt'] = pw_info['salt']
	# 				member_data['hash'] = pw_info['hash']
	# 		#need to handle internal errors
	# 		validations['all_valid'] = all_valid
	# 		validations['validated_data'] = member_data
	# 	except:
	# 		e = sys.exc_info()[:0]
	# 		all_valid = False
	# 		validation['int_errors'].append('Model Class: There was a problem when validating data. {}'.format(e))
	# 	return validations
