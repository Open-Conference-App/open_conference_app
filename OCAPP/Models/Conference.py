import time
from flask import flash
from OCAPP.Schema.Conference import Conference
from OCAPP import app, db


def index():
	return db.query(Conference).all()

def create(fields):
	is_valid = True
	for k, v in fields.items():
		if not v:
			flash('All fields are required', 'conf_create_err')
			return False
	if len(fields['year']) != 4:
		is_valid = False
		flash('Year should be formatted 20XX', 'conf_create_err')
	if time.strptime(fields['date']) >= time.time():
		is_valid = False
		flash('Conference date must be in the future.', 'conf_create_err')
	if fields['full_prof_cost'] < 0 or fields['day_prof_cost'] < 0:
		is_valid = False
		flash('Professional conference prices must be positive.', 'conf_create_err')		
	if fields['full_stud_cost'] < 0 or fields['day_stud_cost'] < 0:
		is_valid = False
		flash('Professional conference prices must be positive.', 'conf_create_err')
	if fields['vend_cost'] < 0:
		is_valid = False
		flash('Vendor conference prices must be positive.', 'conf_create_err')
	return is_valid

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

