from flask import Flask
import binascii, os
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATETIME, BOOLEAN
from OCAPP import app, Base, BaseChanges
from OCAPP.Models import Member  
from OCAPP.Models.BaseChanges import BaseChanges

class PasswordReset(BaseChanges, Base):
	__tablename__ = 'password_resets'
	id = Column(INTEGER(11), primary_key=True)
	member_id = Column(INTEGER(11), ForeignKey('members.id'))
	member = relationship('Member')
	reset_hash = Column(VARCHAR(255))
	created_at = Column(DATETIME(), default=func.utc_timestamp())
        updated_at = Column(DATETIME(), default=func.utc_timestamp(), onupdate=func.utc_timestamp())

	def __init__(self, data):
		self.member_id = data['id']
		self.reset_hash = binascii.hexlify(os.urandom(32))
	def __repr__(self):
                return '<PasswordReset(member_id=%r, hash=%r>' % (self.member_id, self.reset_hash)

