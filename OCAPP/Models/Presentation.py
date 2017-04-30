from OCAPP.Schema.Presentation import Presentation
from OCAPP.Models import Member, Conference

from OCAPP.Schema.PresentationType import PresentationType
from OCAPP import SQLEZ, rollback, savepoint
db = SQLEZ()
from sqlalchemy import inspect

import json, binascii, os, csv, codecs, cStringIO

def create(pres_data):
	return db.create(Presentation, pres_data)

def get_types():
	return db.query(PresentationType).all()

def get_by_id(id):
	return db.get(Presentation, id)
def output_csv():
	presentations = db.query(Presentation).all()
	presentation_csv = open("../presentations.csv", "w")
	writer = csv.writer(presentation_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(['Title', 'Summary', 'Type', 'Presenter 1', 'Presenter 2','Presenter 3', 'Presenter 4'])
	for pres in presentations:
		values = []
		values.append(pres.title)
		values.append(pres.summary)
		values.append(pres.type.name)

		num_presenters = 1
		print pres.nonmember_presenters
		if pres.nonmember_presenters:
			nonmembers = json.loads(pres.nonmember_presenters)
			for presenter in nonmembers:
				values.append(presenter["fname"] + ' ' + presenter["lname"] + ' (' + presenter["email"] + ')')
				num_presenters += 1
		if pres.presenters:
			for member in pres.presenters:
				values.append(member.first_name + ' ' + member.last_name + ' (' + member.email + ')')
				num_presenters += 1
		writer.writerow([c.encode("utf-8") for c in values])
	presentation_csv.close()

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

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
