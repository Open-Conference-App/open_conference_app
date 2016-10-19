from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME
from OCAPP import app

from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()
engine = create_engine(sens.db_path)

class Institution(Base):
	__tablename__ = 'institutions'
	id = Column(INTEGER(11), primary_key=True)
	name = Column(VARCHAR(255), unique=True)
	contact_name = Column(VARCHAR(255))
	address_id = Column(INTEGER(11), ForeignKey('addresses.id'))
	members = relationship('Member', backref='institution', lazy='dynamic')
	created_at = Column(DATETIME())
	updated_at = Column(DATETIME())

	def __repr__(self):
		return "<Institution(name=%s)>" % self.name

	def __init__(self, inst_data):
		self.name = inst_data['name']
		self.contact_name = inst_data['contact_name']
		self.created_at = datetime.now()
		self.updated_at = datetime.now()

