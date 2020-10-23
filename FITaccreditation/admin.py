from django.contrib import admin
from .models import *
from django_extensions.admin import ForeignKeyAutocompleteAdmin

# Removes a default model we don't care about
from django.contrib.auth.models import Group
admin.site.unregister(Group)
admin.site.register(Contact)

# Tell admin site which fields to show and base searches on
class UserProfileAdmin(ForeignKeyAutocompleteAdmin):
    exclude = ('user_permissions',)

    list_display = ('email', 'first_name', 'last_name')

    search_fields = ('email', 'first_name', 'last_name')
admin.site.register(UserProfile, UserProfileAdmin)

class CourseAdmin(ForeignKeyAutocompleteAdmin):
    list_display = ('title', 'code', 'program')

    search_fields = ('title', 'code', 'program')
admin.site.register(Course, CourseAdmin)

class OutcomeAdmin(ForeignKeyAutocompleteAdmin):
	list_display = ('key', 'program', 'description')

	search_fields = ('key', 'program', 'description')
admin.site.register(Outcome, OutcomeAdmin)