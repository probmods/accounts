from django.conf.urls import patterns, include, url
from auth.views import index, home, log_in, register, log_out,all_exercises, each_exercise
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index, name="index"),
    url(r'^home$', home, name="home"),
    url(r'^admin', include(admin.site.urls)),
    url(r'^code', include('user_code.urls', namespace="user_code")),
)


urlpatterns += patterns('',
    url(r'^login$', log_in, name="log_in"),
    url(r'^register$', register, name="register"),
    url(r'^logout$', log_out, name="log_out"),
)

urlpatterns += patterns('',
    url(r'^exercise/_all$', all_exercises, name ='all_exercises'),
    url(r'^exercise/(?P<string>[-\w]+)$', each_exercise, name ='each_exercise'),
)