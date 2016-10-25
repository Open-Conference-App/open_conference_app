from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from sqlalchemy.sql import func
from OCAPP import app, db
from OCAPP.Models.Conference import vendor_conferences
from OCAPP.Models.BaseChanges import BaseChanges

class Vendor(BaseChanges, db.Base):
	__tablename__ = 'vendors'
	id = Column(INTEGER(11), primary_key=True)
	name = Column(VARCHAR(255), unique=True)
	address_id = Column(INTEGER(11), ForeignKey('addresses.id'))
	contact_name = Column(VARCHAR(255))
	contact_email = Column(VARCHAR(255))
	contact_phone = Column(VARCHAR(15))
	conferences = relationship('Conference', secondary=vendor_conferences, backref=backref('conf_vendors', lazy='dynamic'))
	created_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())
	updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())
	
	def __init__(self, vend_info):
		self.name = vend_info['name']
		self.address_id = vend_info['address_id']
		self.contact_name = vend_info['contact_name']
		self.contact_email = vend_info['contact_email']
		self.contact_phone = vend_info['contact_phone']
		# self.conferences.append()

