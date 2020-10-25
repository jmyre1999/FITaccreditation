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
