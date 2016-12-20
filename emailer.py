#!/usr/bin/env python
# Simple emailer script
import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

config = ConfigParser.ConfigParser()
"""
Example: config file, located in /home/<user>/.emailrc
[config]
user = test
password = banana
"""
config.read('')									# path to config variables
email_user = config.get('config', 'user')		# gets the user variable
email_pass = config.get('config', 'password')	# gets the password variable
mailing_list = ['']								# who to send emails to

def send_email(message):
	try:
		# gmail account must allow access https://www.google.com/settings/security/lesssecureapps
		emailserver = smtplib.SMTP('smtp.gmail.com', 587)
		emailserver.starttls()
		emailserver.login(email_user, email_pass)
		for i in mailing_list:
			msg = MIMEMultipart()
			msg['From'] = email_user
			msg['To'] = i
			msg['Subject'] = 'Alert script'
			body = message
			msg.attach(MIMEText(body, 'plain'))
			text = msg.as_string()
			emailserver.sendmail(email_user, i, text)
		emailserver.quit()
	except:
		print "Failed to send email(s)"
	return

if __name__ == "__main__":
	send_email("message of what to send")
