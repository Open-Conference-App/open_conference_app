from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, db
from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
engine = create_engine(sens.db_path)
from OCAPP.Models.BaseChanges import BaseChanges

class State(BaseChanges, db.Base):
	__tablename__ = 'states'
	id = Column(INTEGER(11), primary_key=True)
	abbrev = Column(VARCHAR(2))
	addresses = relationship('Address', back_populates='state')
	
	def __init__(self, abbrev):
		self.abbrev = abbrev
