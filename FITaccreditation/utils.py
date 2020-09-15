# This file is for python functions
from django.contrib.auth import authenticate, login, logout

def sum(x, y):
	return x+y

def login_user(request, email, password):
	user = authenticate(email=email.lower(), password=password)
	print(user)
	if user != None:
		login(request, user)
		return True
	else:
		return False