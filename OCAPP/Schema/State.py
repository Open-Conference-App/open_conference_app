from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, Base, BaseChanges
from OCAPP.config import sensitive
sens = sensitive.Sens()

class State(BaseChanges, Base):
	__tablename__ = 'states'
	id = Column(INTEGER(11), primary_key=True)
	abbrev = Column(VARCHAR(2))
	addresses = relationship('Address', back_populates='state')
	
	def __init__(self, abbrev):
		self.abbrev = abbrev
