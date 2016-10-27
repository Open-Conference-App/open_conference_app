import os
class Sens:
	def __init__(self):
		self.root_path = "root/path/here"
		self.db_path = 'db/path/here'
		self.secret_key = "generate/some/random/string/here"
		self.google_drive_key = self.root_path + 'path/to/json/file' #json file required for drive API v3
		self.drive_root_folder_id = 'Google Drive folder id' #folder id for presentation files to be stored in
		self.stripe_secret_key = 'Stripe secret key' #private key for stripe -- CURRENTLY IN TEST

	def gen_csrf_token(self):
		return os.urandom(24).encode('hex')
