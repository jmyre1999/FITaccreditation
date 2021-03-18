# This file is specifically for view functions (aka functions linked to urls)
# If you need to make a backend function, make it in utils.py and include it here

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect, HttpResponse, Http404
from wsgiref.util import FileWrapper
from io import StringIO
from django.core.files.storage import default_storage
import os
from FITaccreditation.utils import *
from FITaccreditation.models import *
from django_ajax.decorators import ajax
from django.core.mail import send_mail
from django.conf import settings

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
			if request.user.role == 'RE':
				return HttpResponseRedirect('/dashboard/')
			elif request.user.role == 'FA':
				return HttpResponseRedirect('/reviewer_dashboard/')
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
					os.environ.get('EMAIL_HOST_USER', ''),
					[os.environ.get('EMAIL_HOST_USER', ''),],
					fail_silently=False,
				)
				send_mail(
					'FIT Accreditation Assessment Registration',
					'''
					Thank you for registering for faculty status at cse-assessment-test.fit.edu.
					We would like to confirm that you are responsible for this registration so that an administrator may verify your account.
					Please reply with your confirmation, or let us know if you did not create this registration.

					FIT Accreditation Assessment Adminstrators
					http://cse-assessment-test.fit.edu/
					''',
					os.environ.get('EMAIL_HOST_USER', ''),
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
			outcome_pks = request.POST.getlist('outcome', '')
			comment = request.POST.get('comment', '')
			if len(outcome_pks) > 0:
				if request.FILES:
					upload_files = request.FILES.getlist('upload')
					for upload_file in upload_files:
						file_name,file_ext = os.path.splitext(upload_file.name)
						if (file_ext not in [".exe",".EXE",".bat",".BAT"]):
							artifact = Artifact.objects.create(upload_file=upload_file, course=course, comment=comment, uploader=request.user)
							for outcome_pk in outcome_pks:
								outcome = Outcome.objects.get(pk=int(outcome_pk))
								artifact.outcome.add(outcome)
								artifact.save()
								if SatisfiedOutcome.objects.filter(course=course, outcome=outcome, archived=False).exists():
									satisfied_outcome = SatisfiedOutcome.objects.filter(course=course, outcome=outcome, archived=False).last()
								else:
									satisfied_outcome = SatisfiedOutcome.objects.create(course=course, outcome=outcome, archived=False)
									satisfied_outcome.artifacts.add(artifact)
									satisfied_outcome.save()
						else:
							if not error:
								error_message = 'The following files were denied: ' + file_name + file_ext
							else:
								error_message = error_message + ", " + file_name + file_ext
							error = True
					if not error:	
						return redirect('/success_survey/')
				else:
					error = True
					error_message = 'No file uploaded'
			else:
				error = True
				error_message = 'No outcomes applied'
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
		unsatisfied_outcome_pks = selected_course.get_unsatisfied_outcome_pks()
		outcomes_list = []
		for outcome in outcomes:
			if outcome.pk in unsatisfied_outcome_pks:
				satisfied = False
			else:
				satisfied = True
			outcomes_list.append({'pk': str(outcome.pk), 'name': str(outcome), 'description': str(outcome.description), 'satisfied': satisfied,})
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
		image_name,image_extension = os.path.splitext(image.name)
		if image_extension in ['.JPG', '.TIF', '.PNG', '.GIF', '.JPEG', '.jpg', '.tif', '.png', '.jpeg', '.gif']:
			user.image = image
			user = request.user
			user.save()
	return render(request, "account_settings.html")

def notfound_handler(request):
	return render(request, "404.html")

def forbidden_handler(request):
	return render(request, "403.html")

def successful_submission_handler(request):
	return render(request, "success.html")

def successful_submission_survey_handler(request):
	return render(request, "success_survey.html")

def overview(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	if request.user.role in ['']:
		return HttpResponseRedirect('/')

	artifact_objects = Artifact.objects.all()
	artifacts = []
	for artifact in artifact_objects:
		artifact_info = {}
		artifact_info["id"] = artifact.pk
		artifact_info["upload_file"] = artifact.upload_file
		artifact_info["outcome"] = artifact.outcome
		artifact_info["course"] = artifact.course
		artifact_info["uploader"] = artifact.uploader.get_full_name()
		if artifact_info["uploader"] == " ":
			artifact_info["uploader"] = artifact.uploader.email
		artifact_info["upload_date"] = artifact.date_created
		artifact_info["comment"] = artifact.comment
		artifacts.append(artifact_info)
	return render(request, "overview.html", {
		"artifacts":artifacts
		})

def download_artifact(request, artifact_id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	if request.user.role in ['']:
		return HttpResponseRedirect('/')

	download_artifact = Artifact.objects.get(pk=artifact_id)
	download_file = download_artifact.upload_file
	file_path = os.path.join(settings.MEDIA_ROOT,download_file.name)
	print(file_path)
	with default_storage.open(file_path) as fh:
		response = HttpResponse(fh.read(),content_type="application/upload_file")
		response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
		return response

	raise Http404

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
		unsatisfied_outcome_pks = course.get_unsatisfied_outcome_pks()
		outcome_info_list = []
		for outcome in course.outcomes.all():
			outcome_info = {}
			outcome_info['name'] = str(outcome)
			if outcome.pk in unsatisfied_outcome_pks:
				outcome_info['satisfied'] = False
			else:
				outcome_info['satisfied'] = True
			outcome_info['description'] = outcome.description
			outcome_info_list.append(outcome_info)
		course_list.append({'title': course.title, 'pk': course.pk,'unsatisfied_outcomes': course_unsatisfied, 'percent_complete': course_percent, 'outcome_info_list': outcome_info_list,})
	return render(request, "dashboard.html", {
		'user_name': user_name,
		'total_unsatisfied': total_unsatisfied,
		'total_percent': total_percent,
		'course_list': course_list,
		})

def reviewer_dashboard(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/login/')
	if request.user.role in ['','FA']:
		return HttpResponseRedirect('/')

	message = None
	error = False

	if request.POST:
		if request.POST.get('action', '') == 'remind_all':

			message = "Successfully sent reminder email to faculty."

	all_satisfied = True
	outcomes = Outcome.objects.all()
	outcome_list = []
	for outcome in outcomes:
		outcomeinfo = {}
		satisfied_outcomes = SatisfiedOutcome.objects.filter(archived=False,outcome=outcome)
		artifacts = []
		for satisfied_outcome in satisfied_outcomes:
			for artifact in satisfied_outcome.artifacts.all():
				artifacts.append(artifact)
		outcomeinfo["artifacts"] = artifacts
		outcomeinfo["name"] = str(outcome)
		outcomeinfo["description"] = outcome.description
		outcomeinfo["pk"] = outcome.pk
		courses = Course.objects.filter(outcomes__pk=outcome.pk)
		if courses:
			num_complete = 0
			for course in courses:
				if satisfied_outcomes.filter(course=course).exists():
					num_complete = num_complete + 1
			outcomeinfo["percent_complete"] = int(100 * num_complete/courses.count())
			if outcomeinfo["percent_complete"] != 100:
				all_satisfied = False
		else:
			outcomeinfo["percent_complete"] = 100
		outcome_list.append(outcomeinfo)

	return render(request, "reviewer_dashboard.html",{
		"outcome_list": outcome_list,
		'all_satisfied': all_satisfied,
		'error': error,
		'message': message,
		})
