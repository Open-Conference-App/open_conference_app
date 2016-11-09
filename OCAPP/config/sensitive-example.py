import os
class Sens:
	def __init__(self):
		self.root_path = "root/path/here"
		self.db_path = 'mysql+mysqldb://<username>:<pw>@IP/domain:<port>/directory_of_installation'
		self.secret_key = "generatSomeRandomStringHere"
		self.google_drive_key = self.root_path + 'path/to/json/file' #json file required for drive API v3
		self.drive_root_folder_id = 'Google Drive folder id' #folder id for presentation files to be stored in
		self.stripe_secret_key = 'Stripe secret key' #private key for stripe -- CURRENTLY IN TEST
