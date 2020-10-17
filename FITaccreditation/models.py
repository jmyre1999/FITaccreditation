from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models

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

class UserProfile(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=75, db_index=True, unique=True)
	first_name = models.CharField(max_length=25, blank=True)
	last_name = models.CharField(max_length=25, blank=True)
	image = models.ImageField(upload_to='userprofile', null=True, blank=True, max_length=500)
	is_staff = models.BooleanField(default=False)
	is_faculty = models.BooleanField(default=False)

	objects = UserProfileManager()

	USERNAME_FIELD =  'email'

	# When converting to string, return user's email
	def __str__(self):
		return self.email

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

class Contact(models.Model):
	name = models.CharField(max_length = 200)
	email = models.EmailField()
	subject = models.TextField()
	def __str__(self):
		return self.name