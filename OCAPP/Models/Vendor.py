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

from OCAPP.Models.Conference import vendor_conferences

class Vendor(Base):
	__tablename__ = 'vendors'
	id = Column(INTEGER(11), primary_key=True)
	name = Column(VARCHAR(255), unique=True)
	address_id = Column(INTEGER(11), ForeignKey('address.id'))
	contact_name = Column(VARCHAR(255))
	conferences = relationship('Conference', secondary=vendor_conferences, backref=backref('vendors', lazy='dynamic'))
	created_at = Column(DATETIME())
	updated_at = Column(DATETIME())

