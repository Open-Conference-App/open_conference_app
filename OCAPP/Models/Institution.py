from flask_sqlalchemy import SQLAlchemy
from OCAPP.Schema.Institution import Institution
from OCAPP import app, db

def index():
	return db.query(Institution).all()

def show(inst_id):
	return Institution.query.get(inst_id)

def create(inst_data):
	return db.create(Institution, inst_data)

def delete(inst_id):
	return ''


def update(inst_data):
	inst = Institution.query.get(inst_data['id'])
	return inst

#/institutions #get
#/institutions/<inst_id> #get
#/institutions/new #get
#/institutions/<inst_id>/delete #get
#/institutions/<inst_id> #put/patch
