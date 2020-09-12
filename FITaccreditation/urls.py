from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from FITaccreditation import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
]
