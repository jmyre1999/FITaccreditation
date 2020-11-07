from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
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
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)