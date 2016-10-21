from flask import Flask, session
from OCAPP.config import sensitive
sens = sensitive.Sens()
app = Flask('OCAPP', static_folder=sens.root_path + '/assets/static', template_folder=sens.root_path + '/assets/templates')
app.secret_key = sens.secret_key
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

class SQLEZ:
	def __init__(self):
		self.Base = declarative_base()
		self.engine = create_engine(sens.db_path)
		Session = sessionmaker(bind=self.engine)
		self.session = Session() 

db = SQLEZ()
from OCAPP.Models.Valids import Valids
valids = Valids()

# from OCAPP.Models import State, Address, Institution, Conference, Member, Presentation, Vendor
# db.Base.metadata.create_all(db.engine)
from OCAPP.Models.State import State
from OCAPP.Models.Address import Address
from OCAPP.Models.Institution import Institution
from OCAPP.Models.Member import Member
from OCAPP.Models.Conference import Conference, MemberConferences
from OCAPP.Models.Presentation import Presentation
from OCAPP.Models.Vendor import Vendor

















