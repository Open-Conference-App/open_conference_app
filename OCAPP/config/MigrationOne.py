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
from OCAPP.Schema import State,Address,Institution, Member, Conference, PresentationType
from OCAPP import db
import datetime, os, binascii, hashlib

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA","KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH","NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX","UT", "VT", "VA", "WA", "WV", "WI", "WY"]
for state in states:
	state = State.State(state)
	db.session.add(state)

addy = Address.Address({
	'street1': '1010 Birchwood Lane',
	'street2': '',
	'city': 'Mansfield',
	'state_id': 43,
	'zip': '76063' 
})

db.session.add(addy)


inst = Institution.Institution({
	'name': 'University of Colorado Boulder'
})

db.session.add(inst)

salt = binascii.hexlify(os.urandom(16))
hash = hashlib.sha256(salt + 'Swons789.').hexdigest()
mem = Member.Member({
	'first_name':'Ryan',
	'last_name': 'Culpepper',
	'address_id': 1,
	'email': 'ryan.culpepper@gmail.com',
	'salt': salt,
	'hash':hash,
	"type": 'Professional',
	"officer": True
})
mem.institution = inst
db.session.add(mem)


conf = Conference.Conference({
	"year": "2017",
	"prof_cost": 70,
	"stud_cost": 40,
	"vend_cost": 50,
	"start_date": datetime.date(2017,4,28),
	"end_date": datetime.date(2017,4,29),
	"title": "(Em)Powering Language Teaching and Learning with Technology"
	})
conf.host = mem
conf.institution = inst
db.session.add(conf)

types = {
'Individual/Group Presentation': ['Typically, presenters share information before a group in a classroom / lecture room setting.', 30],
'Workshop': ['Workshops are usually done in a computer lab (or BYOD if the proposal description calls for it). Participants have meaningful hands on time to interact with technology.', 60],
'Demonstration': ['Demonstration sessions are typically given by vendors of language technology products relevant to teaching and learning languages in academic settings such as K12 schools and colleges and universities.', 30],
'Panel Discussion': ['Typically, a panel discussion is a small group of individuals who respond to various questions and prompts. Each participant has time to react to these questions and prompts. Panel groups are organized by the member submitting the proposal. Specify the desired length (30 or 60 min) in your proposal.', 60],
'Technology Test Kitchen': ["We invite anyone to participate as 'tech chefs' in the technology test kitchen! In this session, there will be multiple facilitators, each at their own table. They will demonstrate a product (giving hands on time to a small group) in round robin style. After 10 minutes, attendees at one table will switch to the next to encounter another demonstration. Think of it as a low pressure, hands on 'speed dating' sales pitch for the technology you're demonstrating! We'd like at least one test kitchen session each day, both having at least 6 tables with different demos going on at the same time.", 10]
}

for type, info in types.items():
	pres_type = PresentationType.PresentationType({
		"name": type,
		"description": info[0],
		"duration": info[1]
		})
	db.session.add(pres_type)

db.session.commit()
