import smtplib, os
from flask import render_template
from OCAPP.config.sensitive import Sens
sens = Sens()
from OCAPP import app

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

fromAddy = sens.account_email
username = sens.account_email
password = sens.account_pw

def send(msg):
	server = smtplib.SMTP('smtp.gmail.com:587')
	message = MIMEMultipart('alternative')
	message['Subject'] = msg['subject']
	message['From'] = fromAddy
	message['To'] = msg['toAddy']
	msg['template'] = 'mail/' + msg['template']
	msg['data']['data']['plain_message'] = msg['plain_message']
	if 'data' in msg:
		data = {}
		code = "render_template(msg['template']"
		for name, item in msg['data'].items():
			data[name] = item
			code += ", " + name + "=data['" + name + "']"
		code += ")"
	part1 = MIMEText( message['plain_message'],'plain')
	part2 = MIMEText( eval(code),'html')
	img_data = open(app.static_folder + '/images/SOCALLT.png', 'rb')
	image = MIMEImage(img_data.read())
	img_data.close()
	image.add_header('Content-ID', '<image1>')
	message.attach(part1)
	message.attach(part2)
	message.attach(image)
	server.ehlo()
	server.starttls()
	server.login(username, password)
	server.sendmail(fromAddy, msg['toAddy'], message.as_string())
	print 'mail sent'
	server.quit()



