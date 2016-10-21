import re, os, binascii, hashlib, sys
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_CAP_REGEX = re.compile(r'[A-Z]')
PASS_LOW_REGEX = re.compile(r'[a-z]')
PASS_NUM_REGEX = re.compile(r'\d')
NAME_REGEX = re.compile(r'\d')


class Valids():
	def check_blanks(self,member_data):
		ret_obj = {'all_valid': False, 'blanks': [], 'errors':[], 'int_errors':[]}
		try:
			all_valid = True
			for key, value in member_data.items():
				if not value:
					all_valid = False
					ret_obj['blanks'].append(key)
			ret_obj['all_valid'] = all_valid
		except:
			e = sys.exc_info()[:0]
			all_valid = False
			ret_obj['int_errors'].append('There was a problem when searching for blanks. {}'.format(e))
		ret_obj['all_valid'] = all_valid
		return ret_obj

	def check_email(self,email):
		ret_obj = {'all_valid': False, 'errors':[], 'int_errors':[]}
		try:
			all_valid = True
			EMAIL_REGEX.match(email)
			if EMAIL_REGEX.match(email) == None:
				print 'error with email'
				ret_obj['errors'].append('Email formatted incorrectly.  Please check for errors.')
				all_valid = False
			if db.session.query(Member).filter_by(email=email).first():
				ret_obj['errors'].append('The email you entered already exists in our database.')
				all_valid = False
		except:
			e = sys.exc_info()[:0]
			all_valid = False
			ret_obj['int_errors'].append('There was a problem when validating the email address.  {}'.format(e))
		ret_obj['all_valid'] = all_valid
		return ret_obj

	def process_password(self, password):
		ret_obj = {'all_valid': False, 'errors':[], 'int_errors':[]}
		try:
			all_valid = True
			if len(password) < 9:
				all_valid = False
				ret_obj['errors'].append('Passwords must be at least 9 characters.')
			if not PASS_NUM_REGEX.search(password):
				all_valid = False
				ret_obj['errors'].append('Passwords must contain letters and numbers.')
			if not PASS_CAP_REGEX.search(password):
				all_valid = False
				ret_obj['errors'].append('Passwords must contain at least 1 uppercase letter.')
			if not PASS_LOW_REGEX.search(password):
				all_valid = False
				ret_obj['errors'].append('Passwords must contain at least 1 lowercase letter.')
			if all_valid:
				ret_obj['salt'] = binascii.hexlify(os.urandom(16))
				ret_obj['hash'] = hashlib.sha256(ret_obj['salt'] + password).hexdigest()
		except:
			e = sys.exc_info()[:0]
			all_valid = False
			ret_obj['int_errors'].append('There was a problem when processing the password.  {}'.format(e))
		ret_obj['all_valid'] = all_valid
		return ret_obj

from OCAPP import db
from OCAPP.Models.Member import Member



