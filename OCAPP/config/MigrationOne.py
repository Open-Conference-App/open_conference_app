from OCAPP.config import sensitive
sens = sensitive.Sens()
from flask import Flask, session
app = Flask('OCAPP', static_folder=sens.root_path + '/assets/static', template_folder=sens.root_path + '/assets/templates')
app.secret_key = sens.secret_key
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()
engine = create_engine(sens.db_path)
Session = sessionmaker(bind=engine)
session = Session()
from OCAPP import State,Address,Institution, Member

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA","KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH","NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX","UT", "VT", "VA", "WA", "WV", "WI", "WY"]
for state in states:
	state = State(state)
	session.add(state)

session.commit()
addy = Address({
	'street1': 'Hellems Hall 156',
	'street2': '239 UCB',
	'city': 'Boulder',
	'state_id': 6,
	'zip': '80309' 
})


inst = Institution({
	'name': 'University of Colorado Boulder'
})
mem = Member({
	'first_name':'Mark',
	'last_name': 'Knowles',
	'address_id': 1,
	'email': 'mark.knowles@colorado.edu',
	'password':'Password2017',
	'institution_id':1  
})
