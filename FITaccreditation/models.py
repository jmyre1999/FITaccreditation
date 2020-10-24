from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from datetime import datetime

class UserProfileManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
		    raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_superuser') is not True:
		    raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

CLASS_CHOICES = (
    ('FA', 'Faculty'),
    ('AD', 'Advisor'),
    ('RE', 'Reviewer'),
)

class UserProfile(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=75, db_index=True, unique=True)
	first_name = models.CharField(max_length=25, blank=True)
	last_name = models.CharField(max_length=25, blank=True)
	image = models.ImageField(upload_to='userprofile', null=True, blank=True, max_length=500)
	is_staff = models.BooleanField(default=False)
	is_faculty = models.BooleanField(default=False)
	role = models.CharField(max_length=25, blank=True, choices=CLASS_CHOICES)

	objects = UserProfileManager()

	USERNAME_FIELD =  'email'

	# When converting to string, return user's email
	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

	def get_unsatisfied_outcomes(self):
		user_courses = self.course_set.all()
		outcomes_list = []
		for course in user_courses:
			for outcome in course.outcomes.all():
				if not SatisfiedOutcome.objects.filter(course=course, outcome=outcome, archived=False).exists():
					outcomes_list.append({
										'course': course.title, 
										'outcome': str(outcome), 
										'description': outcome.description,
										})
		return outcomes_list

PROGRAM_CHOICES = (
	('CS', 'Computer Science'),
	('SE', 'Software Engineering'),
)

class Outcome(models.Model):
	key = models.CharField(max_length=1)
	description = models.CharField(max_length=200)
	program = models.CharField(max_length=2, choices=PROGRAM_CHOICES)

	def __str__(self):
		return self.program + ' Outcome ' + self.key

class Course(models.Model):
	title = models.CharField(max_length=50)
	instructors = models.ManyToManyField('UserProfile', blank=True)
	program = models.CharField(max_length=2, choices=PROGRAM_CHOICES)
	code = models.CharField(max_length=4)
	outcomes = models.ManyToManyField('Outcome', blank=True)

	def __str__(self):
		return self.title

	def get_unsatisfied_outcomes(self):
		outcomes_list = []
		for outcome in self.outcomes.all():
			if not SatisfiedOutcome.objects.filter(course=self, outcome=outcome, archived=False).exists():
				outcomes_list.append({
									'outcome': str(outcome), 
									'description': outcome.description,
									})
		return outcomes_list


class SatisfiedOutcome(models.Model):
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	outcome = models.ForeignKey('Outcome', on_delete=models.CASCADE)
	# Artifacts
	date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
	archived = models.BooleanField(default=False)

	def __str__(self):
		return self.course.title + ' ' + str(self.outcome)

class Contact(models.Model):
	name = models.CharField(max_length = 200)
	email = models.EmailField()
	subject = models.TextField()

	def __str__(self):
		return self.name
class Artifact(models.Model):
	title = models.CharField(max_length=50)
	program = models.CharField(max_length=2, choices=PROGRAM_CHOICES)
	course = models.OneToOneField('Course', on_delete=models.CASCADE,blank =True,null = True)
    advisor = models.ForeignKey('UserProfile', related_name='assignment_advisor', on_delete=models.CASCADE)
	assignee = models.ForeignKey('UserProfile', related_name='assignment_assignee', on_delete=models.CASCADE)
	outcome = models.ForeignKey('Outcome', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
	date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	due_date = models.DateTimeField()
	complete = models.BooleanField(default=False)
	date_completed = models.DateTimeField(blank=True)
	
    def __str__(self):
		return self.title
