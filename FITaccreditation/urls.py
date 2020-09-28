from django.contrib import admin
from django.urls import path
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
    url(r'^account_settings/$', views.account_settings, name='account_settings'),
    url(r'^hello/$', views.hello, name='hello'),
]
