from flask import Flask
import imp, re, hashlib, binascii, os, datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from OCAPP import app
from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)
Base = declarative_base()

class Address(Base):
	__tablename__ = 'addresses'
	id = Column(INTEGER(11), primary_key=True)
	street1 = Column(VARCHAR(255))
	street2 = Column(VARCHAR(255))
	city = Column(VARCHAR(255))
	state_id = Column(INTEGER(11), ForeignKey('states.id'))
	zip = Column(VARCHAR(5))

	def __init__(self, address_data):
		self.street1 = address_data['street1']
		self.street2 = address_data['street2']
		self.city = address_data['city']
		self.state_id = address_data['state_id']
		self.zip = address_data['zip']

Base.metadata.create_all(engine)
