import time
from flask import flash
from OCAPP.Schema.Conference import Conference, Registration
from OCAPP.Models import Member 
from OCAPP import app, SQLEZ
db = SQLEZ()


def index():
	return db.query(Conference).order_by(Conference.year.desc()).all()

def create(fields):
	return ''

def get_by_id(id):
	conference = db.get(Conference, id)
	if not conference:
		conference = get_next()
	return conference

def get_next():
	return db.query(Conference).order_by(Conference.year.desc()).first()

def get_prices(id):
	conf = db.get(Conference, id)
	return {
		'stud_cost': conf.stud_cost,
		'prof_cost': conf.prof_cost,
		'vend_cost': conf.vend_cost,
		}
def destroy(id):
	return db.delete(Conference, id)

def update(conference, up_conf):
	for key in conference.keys():
		if conference[key] != up_conf[key]:
			conference[key] = up_conf[key]
	return conference

def register(id, member,data):
	conf = db.get(Conference, id)
	registration = Registration(data);
	registration.conference = conf
	registration.member = member
	registration.days = data['days']
	registration.type = data['type']
	db.session.add(registration)
	db.session.commit()
	return conf

def set_transaction(conf_id, member_id, transaction_id):
	conf = db.get(Conference, conf_id)
	memb = Member.get_by_id(member_id)
	for registration in conf.registrations:
		if registration.member_id == memb.id:
			registration.transaction_id = transaction_id
			registration.member_paid = True
			memb.active = True
			db.session.add(registration)
			db.session.commit()
	return member_conf.member_paid 

def members(conf_id):
	conf = get_by_id(conf_id)
	members = [];
	for registration in conf.registrations:
		memb = Member.get_by_id(registration.member_id)
		if(memb):
			members.append(memb)
	return members






