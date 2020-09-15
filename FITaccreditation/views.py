# This file is specifically for view functions (aka functions linked to urls)
# If you need to make a backend function, make it in utils.py and include it here

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect
import os
from FITaccreditation.utils import *
from FITaccreditation.models import *

def home(request):
	print("This is is the home view")
	test_string = "This is a test"
	print("utils test:")
	print("3 + 5 = ", sum(3,5))
	print("request test:")
	print(request)
	return render(request, "home.html", {
		'test_string': test_string, # 'front_end_name': back_end_name,

		})

def eac_criteria(request):
	return render(request, "eac-criteria.html")

def cac_criteria(request):
	return render(request, "cac-criteria.html")

def login_form(request):
	error = False
	error_message = ""
	if request.POST:
		email = request.POST.get('email', '').lower()
		password = request.POST.get('password', '')
		error = not login_user(request, email, password)
		if error:
			error_message = "There is no user matching the given email and password"
		else:
			return HttpResponseRedirect('/')

	return render(request, "login.html", {
		'error': error,
		'error_message': error_message,
		})

def logout_user(request):
	error = False
	error_message = ""
	user = request.user
	if user != None:
		logout(request)
	return HttpResponseRedirect('/')

def register_form(request):
	error = False
	error_message = ""
	if request.POST:
		email = request.POST.get('email', '').lower()
		password = request.POST.get('password', '')
		if UserProfile.objects.filter(email__iexact=email):
			error = True
			error_message = "A user with that email address already exists"
		else:
			user = get_user_model().objects.create_user(email, password)
			user.save()
			login_user(request, email, password)
	return render(request, "register.html", {
		'error': error,
		'error_message': error_message,
		})

def submission(request):
	return render(request, "submission.html")

def account_settings(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')
	if request.POST:
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		user = request.user
		if first_name != '':
			user.first_name = first_name.capitalize()
		if last_name != '':
			user.last_name = last_name.capitalize()
		user.save()
	return render(request, "account_settings.html")

