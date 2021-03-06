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
	is_active = models.BooleanField(default=True)
	role = models.CharField(max_length=25, blank=True, choices=CLASS_CHOICES)

	objects = UserProfileManager()

	USERNAME_FIELD =  'email'

	# When converting to string, return user's email
	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

	def get_display_name(self):
		if self.first_name != '' and self.last_name != '':
			return get_full_name()
		else:
			return str(email)

	def get_unsatisfied_courses(self):
		user_courses = self.course_set.all()
		course_list = []
		for course in user_courses:
			if not SatisfiedOutcome.objects.filter(course=course, archived=False).exists():
				course_list.append(course)
		return course_list

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

	def get_all_outcomes(self):
		user_courses = self.course_set.all()
		outcomes_list = []
		for course in user_courses:
			for outcome in course.outcomes.all():
				outcomes_list.append({
									'course': course.title, 
									'outcome': str(outcome), 
									'description': outcome.description,
									})
		return outcomes_list

PROGRAM_CHOICES = (
	('CS', 'Computer Science'),
	('SE', 'Software Engineering'),
	('CE', 'Computer Science and Software Engineering')
)

class Outcome(models.Model):
	key = models.CharField(max_length=1)
	description = models.CharField(max_length=300)
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

	def get_unsatisfied_outcome_pks(self):
		outcomes_list = []
		for outcome in self.outcomes.all():
			if not SatisfiedOutcome.objects.filter(course=self, outcome=outcome, archived=False).exists():
				outcomes_list.append(outcome.pk)
		return outcomes_list

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
	artifacts = models.ManyToManyField('Artifact', blank=True)
	date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	last_updated = models.DateTimeField(auto_now=True, blank=True, null=True)
	archived = models.BooleanField(default=False)

	def __str__(self):
		return self.course.title + ' ' + str(self.outcome)

class Contact(models.Model):
	name = models.CharField(max_length = 200)
	email = models.EmailField()
	subject = models.TextField()
	user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.name

# Instances of student work
class Artifact(models.Model):
	upload_file = models.FileField(upload_to='artifacts', max_length=500)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	outcome = models.ManyToManyField('Outcome',blank=True, null=True)
	comment = models.TextField(default='')
	date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	uploader = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

	def __str__(self):
		return str(self.upload_file)

	def get_artifact_set(self):
		try:
			return self.artifactset_set.first()
		except:
			return None

	def delete(self, *args, **kwargs):
		satisfied_outcomes = self.satisfiedoutcome_set.all()
		for satisfied_outcome in satisfied_outcomes:
			satisfied_outcome.artifacts.remove(self)
			if not satisfied_outcome.artifacts.all().exists():
				satisfied_outcome.delete()
		artifact_sets = self.artifactset_set.all()
		for artifact_set in artifact_sets:
			artifact_set.artifacts.remove(self)
		super(Artifact, self).delete(*args, **kwargs)

SET_TYPE_CHOICES = (
	('AS', 'Assignment'),
	('EX', 'Exam'),
	('OT', 'Other')
)

# Exams, Assignments, Other
class ArtifactSet(models.Model):
	name = models.CharField(max_length = 200)
	set_type = models.CharField(max_length=2, choices=SET_TYPE_CHOICES)
	artifacts = models.ManyToManyField('Artifact',blank=True, null=True)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	outcome = models.ManyToManyField('Outcome',blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return str(self.name)

	def display_set_type(self):
		for type_choice in SET_TYPE_CHOICES:
			if self.set_type == type_choice[0]:
				return type_choice[1]
		return ''

	class Meta:
		unique_together = (('name', 'course',),)
