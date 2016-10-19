from flask import Flask, session
from OCAPP.config import sensitive
sens = sensitive.Sens()
app = Flask('OCAPP', static_folder=sens.root_path + '/assets/static', template_folder=sens.root_path + '/assets/templates')
app.secret_key = sens.secret_key
from sqlalchemy.orm import sessionmaker

from OCAPP.Models import State, Address, Member, Institution, Conference, Presentation, Vendor
from OCAPP.config import sensitive
sens = sensitive.Sens()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()
engine = create_engine(sens.db_path)
# from OCAPP.Models.State import State
# from OCAPP.Models.Address import Address
# from OCAPP.Models.Institution import Institution
# from OCAPP.Models.Member import Member
# from OCAPP.Models.Conference import Conference 
# from OCAPP.Models.Presentation import Presentation
# from OCAPP.Models.Vendor import Vendor
Base.metadata.create_all(engine)

# class DB:
# 	def __init__(self):
# 		self.engine = engine













