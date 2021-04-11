# This file is for python functions
from django.contrib.auth import authenticate, login, logout

def login_user(request, email, password):
	user = authenticate(email=email.lower(), password=password)
	print(user)
	if user != None:
		login(request, user)
		return True
	else:
		return False

def check_password_validity(password):
	if len(password) < 8:
		return False
	if not (any(x.isupper() for x in password)):
		return False
	if not (any(x.isdigit() for x in password)):
		return False
	return True

def remind_all_faculty():
	if not os.environ.get('LOCAL_SERVER', None):
		send_mail(
			'Accreditation Reporting Reminder',
			'Email: ' + email,
			os.environ.get('EMAIL_HOST_USER', ''),
			[os.environ.get('EMAIL_HOST_USER', ''),],
			fail_silently=True,
		)
		send_mail(
			'ABET reporting registration',
			'''
			Thank you for registering for faculty status at cse-assessment-test.fit.edu.
			We would like to confirm that you are responsible for this registration so that an administrator may verify your account.
			Please reply with your confirmation, or let us know if you did not create this registration.

			FIT CSE Assessment Adminstrators
			http://cse-assessment-test.fit.edu/
			''',
			os.environ.get('EMAIL_HOST_USER', ''),
			[email,],
			fail_silently=True,
		)