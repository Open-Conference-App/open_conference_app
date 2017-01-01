import smtplib
from OCAPP.config.sensitive import Sens
sens = Sens()

fromAddy = sens.account_email
username = sens.account_email
password = sens.account_pw

def send(toAddy, msg):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username, password)
	server.sendmail(fromAddy, toAddy, msg)
	server.quit()