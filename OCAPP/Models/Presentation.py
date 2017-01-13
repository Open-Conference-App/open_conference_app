from OCAPP.Schema.Presentation import Presentation
from OCAPP.Models import Member, Conference

from OCAPP.Schema.PresentationType import PresentationType
from OCAPP import db, rollback, savepoint

from sqlalchemy import inspect

import json, binascii, os

def create(pres_data):
	return db.create(Presentation, pres_data)

def get_types():
	return db.query(PresentationType).all()

def get_by_id(id):
	return db.get(Presentation, id)

def add_presenters(id, presenters):
	# savepoint()
	pres = get_by_id(id)
	nonmember_presenters = []
	try:
		for key, presenter in presenters.items():
			if key != 'num':
				if presenter['is_member']:
					db_presenter = Member.get_by_email(presenter['email'])
					print db_presenter
					pres.presenters.append(db_presenter)
				else:
					presenter_hash = binascii.hexlify(os.urandom(16))
					presenter['hash'] = presenter_hash
					nonmember_presenters.append(presenter)
		if nonmember_presenters:
			pres.nonmember_presenters = json.dumps(nonmember_presenters)
		db.session.add(pres)
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!'
		print pres
		insp = inspect(pres)
		print insp.persistent
		db.session.commit()
		return True

	except:
		rollback()
		raise
		return False

def get_current_proposals():
	conf = Conference.get_next()
	props = db.query(Presentation).filter(Presentation.conference_id == conf.id, Presentation.approved == False).all()

	return props
