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
    list_display = ('title', 'program', 'code')

    search_fields = ('title', 'code', 'program')
admin.site.register(Course, CourseAdmin)

class OutcomeAdmin(ForeignKeyAutocompleteAdmin):
	list_display = ('key', 'program', 'description')

	search_fields = ('key', 'program', 'description')
admin.site.register(Outcome, OutcomeAdmin)

class SatisfiedOutcomeAdmin(ForeignKeyAutocompleteAdmin):
	list_display = ('course', 'outcome', 'date_created', 'archived')

	search_fields = ('outcome__key', 'outcome__program', 'course__title')

	def archive_satisfied_outcomes(self, request, queryset):
		for satisfied_outcome in queryset:
			satisfied_outcome.archived = True
			satisfied_outcome.save()
	archive_satisfied_outcomes.short_description = 'Bulk archive satisfied outcomes'

	actions = [archive_satisfied_outcomes,]
admin.site.register(SatisfiedOutcome, SatisfiedOutcomeAdmin)

class ArtifactAdmin(ForeignKeyAutocompleteAdmin):
	list_display = ('course', 'uploader', 'upload_file')

	search_fields = ('outcome__key', 'outcome__program', 'course__title', 'uploader__first_name', 'uploader__last_name', 'uploader__email', 'upload_file__name', 'comment')

	# Override original delete selected so satisfied outcomes are handled
	def delete_selected(self, request, queryset):
		for artifact in queryset:
			artifact.delete()
	delete_selected.short_description = "Delete selected artifacts"

	actions = [delete_selected,]
admin.site.register(Artifact, ArtifactAdmin)
