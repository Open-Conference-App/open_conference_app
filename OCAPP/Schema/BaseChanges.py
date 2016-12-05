import re, os, binascii, hashlib, sys, inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_CAP_REGEX = re.compile(r'[A-Z]')
PASS_LOW_REGEX = re.compile(r'[a-z]')
PASS_NUM_REGEX = re.compile(r'\d')
NAME_REGEX = re.compile(r'\d')

class BaseChanges(object):
	#validation checks: check_blanks, check_email, process_password
	@staticmethod
	def validate(cls, data, funcs=['check_blanks']):
		validations = {'all_valid': False, 'errors': [], 'validated_data': {}, 'int_errors':[]}
		all_valid = True
		requirements = {
			'Address':['street1','street2','city','state_id','zip'],
			'Conference':['institution_id','year','prof_cost','stud_cost','vend_cost','date'],
			'Institution':['name'],
			'Member': ['first_name','last_name', 'address_id','email','institution_id'],
			'Presentation':['title','summary','conference_id','duration','presenters'],
			'State':['abbrev'],
			'Vendor':['name','address_id', 'contact_name','contact_email','contact_phone']
		}
		for method in funcs:
			print type(cls).__name__
			if type(cls).__name__ in requirements and method in requirements[type(cls).__name__]:
				info = method(data)
				if not info['all_valid']:
					all_valid = False
					for error in info['int_errors']:
						validations['int_errors'].append(error)
					for error in info['errors']:
						validations['errors'].append(error)
				if method == 'process_password':
					data['salt'] = info['salt']
					data['hash'] = info['hash']
			else:
				validations['errors'].append('The field provided is not required.  Please only provide required fields.')
		validations['all_valid'] = all_valid
		validations['validated_data'] = data
		return validations
	@staticmethod
	def check_blanks(data):
		ret_obj = {'all_valid': False, 'blanks': [], 'errors':[], 'int_errors':[]}
		try:
			all_valid = True
			for key, value in data.items():
				if not value:
					all_valid = False
					ret_obj['blanks'].append(key)
			ret_obj['all_valid'] = all_valid
		except:
			e = sys.exc_info()[:0]
			all_valid = False
			ret_obj['int_errors'].append('Valids Class: There was a problem when searching for blanks. {}'.format(e))
		ret_obj['all_valid'] = all_valid
		return ret_obj
	@staticmethod
	def check_email(data):
		ret_obj = {
			'all_valid': False,
			'errors':[],
			'int_errors':[]
			}
		try:
			all_valid = True
			EMAIL_REGEX.match(data['email'])
			if EMAIL_REGEX.match(data['email']) == None:
				ret_obj['errors'].append('Email formatted incorrectly.  Please check for errors.')
				all_valid = False
			if db.session.query(self).filter_by(email=data['email']).first():
				ret_obj['errors'].append('The email you entered already exists in our database.')
				all_valid = False
		except:
			e = sys.exc_info()[:0]
			all_valid = False
			ret_obj['int_errors'].append('Valids Class: There was a problem when validating the email address.  {}'.format(e))
		ret_obj['all_valid'] = all_valid
		return ret_obj
	@staticmethod
	def process_password(self,data):
		ret_obj = {'all_valid': False, 'errors':[], 'int_errors':[]}
		try:
			all_valid = True
			if len(password) < 9:
				all_valid = False
				ret_obj['errors'].append('Passwords must be at least 9 characters.')
			if not PASS_NUM_REGEX.search(data['password']):
				all_valid = False
				ret_obj['errors'].append('Passwords must contain letters and numbers.')
			if not PASS_CAP_REGEX.search(data['password']):
				all_valid = False
				ret_obj['errors'].append('Passwords must contain at least 1 uppercase letter.')
			if not PASS_LOW_REGEX.search(data['password']):
				all_valid = False
				ret_obj['errors'].append('Passwords must contain at least 1 lowercase letter.')
			if all_valid:
				ret_obj['salt'] = binascii.hexlify(os.urandom(16))
				ret_obj['hash'] = hashlib.sha256(ret_obj['salt'] + data['password']).hexdigest()
		except:
			e = sys.exc_info()[:0]
			all_valid = False
			ret_obj['int_errors'].append('Valids Class: There was a problem when processing the password.  {}'.format(e))
		ret_obj['all_valid'] = all_valid
		return ret_obj
	@staticmethod
	def process_date(self, data):
		##should convert dates from strings in JSON to Python Date objects
		pass

	def


from OCAPP import db
# from OCAPP.Models.Member import Member

