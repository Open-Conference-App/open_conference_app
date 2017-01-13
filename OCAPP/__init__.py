from flask import Flask, session
from flask.ext.seasurf import SeaSurf
from OCAPP.config.sensitive import Sens
sens = Sens()
app = Flask('OCAPP', static_folder=sens.root_path + '/assets/static', template_folder=sens.root_path + '/assets/templates')
app.secret_key = sens.secret_key
csrf = SeaSurf(app)
# from raven.contrib.flask import Sentry
# sentry = Sentry(app, dsn='https://b0e8b593f1fd45b89b29bc3675cb3807:ad556a25e6a54c98be03bbcfef090a80@sentry.io/111734')

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sys
from flask.ext.mail import Mail

mail=Mail(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=587,
	MAIL_USE_SSL=False,
	MAIL_USE_TSL=True,
	MAIL_USERNAME = sens.account_email,
	MAIL_PASSWORD = sens.account_pw,
	DEFAULT_MAIL_SENDER = sens.account_email
	)

mail=Mail(app)

valid_funcs = {
	'Conference': ['check_blanks','process_dates'],
	'Member': ['check_blanks','check_email','process_password']
}
# class Sentry

class SQLEZ:
	def __init__(self):
		self.Base = declarative_base()
		self.engine = create_engine(sens.db_path, echo=True)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()
		self.BaseChanges = {}

	def query(self,cls):
		return self.session.query(cls)

	def create(self, cls, data):
		val_funcs = ['check_blanks'] if cls.__name__ not in valid_funcs else valid_funcs[cls.__name__]
		info = BaseChanges.validate(cls, data, val_funcs) if val_funcs else BaseChanges.validate(cls, data) 
		if info['all_valid']:
			inst = cls(info['validated_data'])
			self.session.add(inst)
			self.session.commit()
			info['validated_data']['id'] = inst.id
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
def savepoint():
	db.session.begin_nested()

def rollback():
	db.session.rollback()

from OCAPP.Models.BaseChanges import BaseChanges
db.BaseChanges = BaseChanges()

# @app.teardown_appcontext
# def teardown_db(exception):
# 	print 'Shutting down DB connection.'
# 	db.engine.close()
# from OCAPP.Models import Address, Vendor, Conference, Institution, Member, Presentation, State, Vendor,PresentationType
# db.Base.metadata.create_all(db.engine)
from OCAPP import routes
# from OCAPP.Schema import State, Address, Institution, Conference, Member, Presentation, Vendor, PresentationType
from OCAPP.Schema.State import State
from OCAPP.Schema.Address import Address
from OCAPP.Schema.Institution import Institution
from OCAPP.Schema.Member import Member
from OCAPP.Schema.Conference import Conference, Registration
from OCAPP.Schema.Presentation import Presentation
from OCAPP.Schema.PresentationType import PresentationType
from OCAPP.Schema.Vendor import Vendor
db.Base.metadata.create_all(db.engine)




















