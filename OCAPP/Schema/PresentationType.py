from flask import Flask
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT

from OCAPP import app, db
from OCAPP.Models.BaseChanges import BaseChanges

class PresentationType(BaseChanges, db.Base):
	__tablename__ = 'presentation_types'
	id = Column(INTEGER(11), primary_key=True)
	name = Column(VARCHAR(255))
	description = Column(TEXT())
	duration = Column(INTEGER(11))
	presentations = relationship('Presentation', back_populates='type')

	def __init__(self, pres_type_info):
		self.name = pres_type_info['name']
		self.description = pres_type_info['description']
		self.duration = pres_type_info['duration']