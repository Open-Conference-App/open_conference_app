from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME
from OCAPP import app, db
import datetime
from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)
from OCAPP.Models.BaseChanges import BaseChanges


class Institution(BaseChanges, db.Base):
	__tablename__ = 'institutions'
	id = Column(INTEGER(11), primary_key=True)
	name = Column(VARCHAR(255), unique=True)
	address_id = Column(INTEGER(11), ForeignKey('addresses.id'))
	address = relationship('Address')
	faculty_members = relationship('Member', back_populates='institution')
	created_at = Column(DATETIME(), default=func.utc_timestamp())
	updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())

	def __repr__(self):
		return "<Institution(name=%s)>" % self.name

	def __init__(self, inst_data):
		self.name = inst_data['name']

