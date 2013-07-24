from django.conf.urls import patterns, include, url
from auth.views import log_in, register, log_out, index, home, all_exercises, each_exercise
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^code/', include('user_code.urls', namespace="user_code")),
    url(r'^home/$', home),
    url(r'^login/$', log_in),
    url(r'^register/$', register),
    url(r'^logout/$', log_out, name="log_out"),
    url(r'^all_exercises/$', all_exercises, name ='all_exercises'),
    url(r'^all_exercises/(?P<string>[-\w]+)/$', each_exercise, name ='each_exercise'),
    
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
