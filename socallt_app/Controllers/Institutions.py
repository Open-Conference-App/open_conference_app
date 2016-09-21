from flask_sqlalchemy import SQLAlchemy
from socallt_app.Models.Institution import Institution
from socallt_app import app, db

def create(inst_data):
	inst = Institution(**inst_data)
	db.session.add(inst)
	db.session.commit()
