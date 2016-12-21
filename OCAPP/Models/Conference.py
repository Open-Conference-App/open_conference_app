import time
from flask import flash
from OCAPP.Schema.Conference import Conference, MemberConferences
from OCAPP.Models import Member 
from OCAPP import app, db


def index():
	return db.query(Conference).all()

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
	mc = MemberConferences(data);
	mc.conference = conf
	mc.member = member
	mc.days = data['days']
	db.session.add(mc)
	db.session.commit()
	return conf

def set_transaction(conf_id, member_id, transaction_id):
	conf = db.get(Conference, conf_id)
	memb = Member.get_by_id(member_id)
	for member_conf in conf.members:
		if member_conf.member_id == memb.id:
			member_conf.transaction_id = transaction_id
			member_conf.member_paid = True
			db.session.add(member_conf)
			db.session.commit()
	return 