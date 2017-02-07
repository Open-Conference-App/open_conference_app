from OCAPP.Schema.State import State
from OCAPP import db

def index():
	return db.query(State).all()
