from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from FITaccreditation import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^cac_criteria/$', views.cac_criteria, name='cac_criteria'),
    url(r'^eac_criteria/$', views.eac_criteria, name='eac_criteria'),
    url(r'^login/$', views.login_form, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.register_form, name='register'),
    url(r'^submission/$', views.submission, name='submission'),
    url(r'^submission/get_outcomes_ajax/$', views.get_outcomes_for_submission, name='submission_outcomes_ajax'),
    url(r'^account_settings/$', views.account_settings, name='account_settings'),
    url(r'^404/$', views.notfound_handler, name='404'),
    url(r'^403/$', views.forbidden_handler, name='403'),
    url(r'^success/$', views.successful_submission_handler, name='success'),
    url(r'^success_survey/$', views.successful_submission_survey_handler, name='success_survey'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^reviewer_dashboard/$', views.reviewer_dashboard, name='reviewer_dashboard'),
    url(r'^overview/$', views.overview, name='overview'),
    url(r'^download_artifact/(?P<artifact_id>\d+)/$', views.download_artifact, name='download_artifact'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
        name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)