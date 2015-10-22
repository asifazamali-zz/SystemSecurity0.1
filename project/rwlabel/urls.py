from django.conf.urls import url
from . import views

urlpatterns = [	
	url(r'^$', views.index, name='index'),
	url(r'^napublic/$', views.napublic, name='napublic'),
	url(r'^naprivate/$', views.naprivate, name='naprivate'),
	url(r'^updatedoc/$', views.updatedoc, name='updatedoc'),


]