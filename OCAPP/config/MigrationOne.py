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
from OCAPP.Schema import State,Address,Institution, Member, Conference
from OCAPP import db
import datetime, os, binascii, hashlib

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA","KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH","NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX","UT", "VT", "VA", "WA", "WV", "WI", "WY"]
for state in states:
	state = State.State(state)
	db.session.add(state)

addy = Address.Address({
	'street1': 'Hellems Hall 156',
	'street2': '239 UCB',
	'city': 'Boulder',
	'state_id': 6,
	'zip': '80309' 
})

db.session.add(addy)


inst = Institution.Institution({
	'name': 'University of Colorado Boulder'
})

db.session.add(inst)

salt = binascii.hexlify(os.urandom(16))
hash = hashlib.sha256(salt + 'Password2017').hexdigest()
mem = Member.Member({
	'first_name':'Mark',
	'last_name': 'Knowles',
	'address_id': 1,
	'email': 'mark.knowles@colorado.edu',
	'salt': salt,
	'hash':hash,
	"type": 'Professional'
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
db.session.commit()
