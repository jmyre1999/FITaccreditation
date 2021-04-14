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
		users = UserProfile.objects.filter(role__in=['FA', 'AD'])
		for user in users:
			unsatisfied_courses = user.get_unsatisfied_courses()
			if len(unsatisfied_courses) > 0:
				user_name = user.get_display_name()
				courses = ""
				counter = 0
				for course in unsatisfied_courses:
					counter += 1
					courses += str(course)
					if counter != len(unsatisfied_courses):
						courses += ", "

				body = '''
					{user_name},

					This is a manual reminder from a faculty advisor.

					You have {num_courses} courses with unsatisied ABET outcomes:
					{courses}.

					Please refer to your progress dashboard for more information: http://cse-assessment-test.fit.edu/submission

					FIT CSE Assessment Adminstrators
					http://cse-assessment-test.fit.edu/
					'''.format(user_name=user_name, num_courses=len(unsatisfied_courses, courses=courses))

				send_mail(
					'ABET reporting reminder',
					body,
					os.environ.get('EMAIL_HOST_USER', ''),
					[user.email,],
					fail_silently=True,
				)

		