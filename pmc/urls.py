from django.conf.urls import patterns, include, url
from auth.views import index, home, log_in, register, log_out,all_exercises, each_exercise
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^home/$', home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^code/', include('user_code.urls', namespace="user_code")),
)


urlpatterns += patterns('',
    url(r'^login/$', log_in),
    url(r'^register/$', register),
    url(r'^logout/$', log_out, name="log_out"),
   
)

urlpatterns += patterns('',
    url(r'^exercises/all$', all_exercises, name ='all_exercises'),
    url(r'^exercises/(?P<string>[-\w]+)/$', each_exercise, name ='each_exercise'),
)