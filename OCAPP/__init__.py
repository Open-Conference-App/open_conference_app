from flask import Flask, session
from flask.ext.seasurf import SeaSurf
from OCAPP.config import sensitive
sens = sensitive.Sens()
app = Flask('OCAPP', static_folder=sens.root_path + '/assets/static', template_folder=sens.root_path + '/assets/templates')
app.secret_key = sens.secret_key
csrf = SeaSurf(app)
from raven.contrib.flask import Sentry
sentry = Sentry(app, dsn='https://b0e8b593f1fd45b89b29bc3675cb3807:ad556a25e6a54c98be03bbcfef090a80@sentry.io/111734')

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

valid_funcs = {
	'Conference': ['check_blanks','process_dates'],
	'Member': ['check_blanks','check_email','process_password']
}
# class Sentry

class SQLEZ:
	def __init__(self):
		self.Base = declarative_base()
		self.engine = create_engine(sens.db_path)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		self.BaseChanges = {}

	def query(self,cls):
		return self.session.query(cls)

	def create(self, cls, data):
		val_funcs = None if type(cls).__name__ not in valid_funcs else valid_funcs[type(cls).__name__]
		info = BaseChanges.validate(cls, data, val_funcs) if val_funcs else BaseChanges.validate(cls, data) 
		if info['all_valid']:
			inst = cls(info['validated_data'])
			self.session.add(inst)
			self.session.commit()
		return info

	def get(self, cls, id):
		return self.query(cls).filter_by(id=id).first()

	def update(self, cls, data):
		#data is a dictionary, with an id and fields to update
		inst = self.query(cls).filter_by(id=data['id']).first()
		valids = []
		for k,v in data.items():				
			if hasattr(inst,k):
				valids.append(k)
			else:
				del data[k]
		info = self.validate(cls, data, valids)
		if info['all_valid']:
			for k,v in info['validated_date'].items():
				setattr(inst,k,v)
		self.session.commit()
		return info

	def delete(self,cls,id):
		inst = self.query(cls).filter_by(id=id).first()
		self.session.delete(inst)
		self.session.commit()
		return id

	def validate(self, cl, data, funcs):
		return BaseChanges.validate(cl, data, funcs)

db = SQLEZ()
from OCAPP.Models.BaseChanges import BaseChanges
db.BaseChanges = BaseChanges()
from OCAPP.Models import Address, Vendor, Conference, Institution, Member, Presentation, State, Vendor
db.Base.metadata.create_all(db.engine)
from OCAPP import routes
# from OCAPP.Models import State, Address, Institution, Conference, Member, Presentation, Vendor
# db.Base.metadata.create_all(db.engine)
# from OCAPP.Models.State import State
# from OCAPP.Models.Address import Address
# from OCAPP.Models.Institution import Institution
# from OCAPP.Models.Member import Member
# from OCAPP.Models.Conference import Conference, MemberConferences
# from OCAPP.Models.Presentation import Presentation
# from OCAPP.Models.Vendor import Vendor



















