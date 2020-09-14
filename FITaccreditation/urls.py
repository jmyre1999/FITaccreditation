from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from FITaccreditation import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^home$', views.home, name='home'),
    url(r'^cac_criteria$', views.cac_criteria, name='cac_criteria'),
    url(r'^eac_criteria$', views.eac_criteria, name='eac_criteria'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^submission$', views.submission, name='submission'),
]
