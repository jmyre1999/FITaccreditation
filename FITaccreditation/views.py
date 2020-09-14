# This file is specifically for view functions (aka functions linked to urls)
# If you need to make a backend function, make it in utils.py and include it here

from django.shortcuts import render, redirect
import os
from FITaccreditation.utils import *

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

def login(request):
	return render(request, "login.html")

def register(request):
	return render(request, "register.html")

def submission(request):
	return render(request, "submission.html")