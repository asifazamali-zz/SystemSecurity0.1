from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','security.views.home',name='home'),
    url(r'^contact/','security.views.contact', name = 'contact'),
    url(r'^about/','project.views.about', name = 'about'),
    url(r'^upload/','security.views.list1', name = 'upload'),
    url(r'^find_friend/','security.views.find_friend', name = 'find_friend'),          
    url(r'^friend/','security.views.friend', name = 'friend'),
    url(r'^notification/','security.views.notification', name = 'notification'),
    url(r'^readnotification/','security.views.readnotification', name = 'read_notification'),
    url(r'^shared/','security.views.shared', name = 'shared'),
    url(r'^save/','security.views.save', name = 'file_save'),
    url(r'^save_details/','security.views.save_details', name = 'save_details'),
    url(r'^update_privacy/','security.views.update_privacy', name = 'update_privacy'),

    url(r'^demo/','security.views.demo', name = 'demo'),    

    url(r'^register/complete/$','security.views.registration_complete',name='registration_complete'),   
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)