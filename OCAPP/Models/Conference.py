import time
from flask import flash
from OCAPP.Schema.Conference import Conference
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

def register(id, member):
	conf = db.get(Conference, id)
	conf.members.append(member)
	db.session.add(conf)
	db.session.commit()
	return conf

