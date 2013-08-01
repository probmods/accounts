from django.conf.urls import patterns, include, url
from auth.views import log_in, register, log_out,all_exercises, each_exercise

urlpatterns = patterns('',
    url(r'^login/$', log_in),
    url(r'^register/$', register),
    url(r'^logout/$', log_out, name="log_out"),
   
)

urlpatterns += patterns('',
    url(r'^exercises/all$', all_exercises, name ='all_exercises'),
    url(r'^exercises/(?P<string>[-\w]+)/$', each_exercise, name ='each_exercise'),
)