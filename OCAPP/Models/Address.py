from OCAPP.Schema.Address import Address
from OCAPP import db

def create(data):
	return db.create(Address, data)

def update(data):
	return db.update(Address, data)

def destroy(data):
	return db.destroy(data['id'])

def get(data):
	return db.get(Address, data['id'])

def index():
	return db.query(Address).all()
