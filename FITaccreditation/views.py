# This file is specifically for view functions (aka functions linked to urls)
# If you need to make a backend function, make it in utils.py and include it here

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect
import os
from FITaccreditation.utils import *
from FITaccreditation.models import *
from django_ajax.decorators import ajax
from django.core.mail import send_mail

def home(request):
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		contact = Contact.objects.create(name=name, email=email, subject=subject)
		if request.user.is_authenticated:
			contact.user = request.user
		contact.save()
		return HttpResponseRedirect('/')
	return render(request, "home.html")

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
		confirm_password = request.POST.get('confirm_password', '')
		if UserProfile.objects.filter(email__iexact=email):
			error = True
			error_message = "A user with that email address already exists"
		elif password != confirm_password:
			error = True
			error_message = "Password does not match"
		elif not check_password_validity(password):
			error = True
			error_message = "Invalid password: Must be 8 or more characters, including one capital letter and a number"
		else:
			user = get_user_model().objects.create_user(email, password)
			user.save()
			if not os.environ.get('LOCAL_SERVER', None):
				send_mail(
					'New Registered User',
					'Email: ' + email,
					os.environ.get('FROM_EMAIL',''),
					[os.environ.get('TO_EMAIL',''),],
					fail_silently=True,
				)
				send_mail(
					'ABET reporting registration',
					'Thank you for registering for faculty status at cse-assessment-test.fit.edu. We would like to confirm that you are responsible for this registrtion so that an administrator may verify your account.',
					os.environ.get('FROM_EMAIL',''),
					[email,],
					fail_silently=True,
				)
			login_user(request, email, password)
	return render(request, "register.html", {
		'error': error,
		'error_message': error_message,
		})

def submission(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	if request.user.role in ['','RE']:
		return HttpResponseRedirect('/')
	error = False
	error_message = ''
	courses = request.user.course_set.all()
	linked_course_pk = int(request.GET.get('linked_course', -1))
	if request.POST:
		course_pk = request.POST.get('course', '')
		if course_pk != '':
			course = Course.objects.get(pk=int(course_pk))
			outcome_pk = request.POST.get('outcome', '')
			if outcome_pk != '':
				outcome = Outcome.objects.get(pk=int(outcome_pk))
				comment = request.POST.get('comment', '')
				if request.FILES:
					upload_file = request.FILES.get('upload')
					artifact = Artifact.objects.create(upload_file=upload_file, course=course, outcome=outcome, comment=comment, uploader=request.user)
					artifact.save()
					if SatisfiedOutcome.objects.filter(course=course, outcome=outcome, archived=False).exists():
						satisfied_outcome = SatisfiedOutcome.objects.filter(course=course, outcome=outcome, archived=False).last()
					else:
						satisfied_outcome = SatisfiedOutcome.objects.create(course=course, outcome=outcome, archived=False)
					satisfied_outcome.artifacts.add(artifact)
					satisfied_outcome.save()
				else:
					error = True
					error_message = 'No file uploaded'
			else:
				error = True
				error_message = 'No outcome selected'
		else:
			error = True
			error_message = 'No course selected'
		
	return render(request, "submission.html", {
		'courses': courses,
		'linked_course_pk': linked_course_pk,
		'error': error,
		'error_message': error_message,
		})

@ajax
def get_outcomes_for_submission(request):
	selected_course_pk = request.POST.get('selected_course_pk')
	if selected_course_pk != '':
		selected_course = Course.objects.get(pk=int(selected_course_pk))
		outcomes = selected_course.outcomes.all()
		outcomes_list = []
		for outcome in outcomes:
			outcomes_list.append({'pk': str(outcome.pk), 'name': str(outcome)})
		return outcomes_list
	return None

def account_settings(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	if request.POST:
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')
		user = request.user
		if first_name != '':
			user.first_name = first_name.capitalize()
		if last_name != '':
			user.last_name = last_name.capitalize()
		user.save()
	if request.FILES:
		image = request.FILES.get('image')
		user.image = image
		user = request.user
		user.save()
	return render(request, "account_settings.html")

def notfound_handler(request):
	return render(request, "404.html")

def dashboard(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	if request.user.role in ['','RE']:
		return HttpResponseRedirect('/')
	user = request.user
	user_name = user.get_full_name()
	if user_name == ' ':
		user_name = user.email
	total_unsatisfied = user.get_unsatisfied_outcomes()
	total_outcomes = user.get_all_outcomes()
	if len(total_outcomes) != 0:
		total_percent = int( (1 - (len(total_unsatisfied)/len(total_outcomes))) * 100)
	else:
		total_percent = 100
	courses = user.course_set.all()
	course_list = []
	for course in courses:
		course_unsatisfied = course.get_unsatisfied_outcomes()
		if course.outcomes.count() != 0:
			course_percent = int( (1 - len(course_unsatisfied)/course.outcomes.count()) * 100)
		else: 
			course_percent = 100
		course_list.append({'title': course.title, 'pk': course.pk,'unsatisfied_outcomes': course_unsatisfied, 'percent_complete': course_percent})
	return render(request, "dashboard.html", {
		'user_name': user_name,
		'total_unsatisfied': total_unsatisfied,
		'total_percent': total_percent,
		'course_list': course_list,
		})
