from django.conf.urls import patterns, include, url
from auth.views import log_in, register, log_out, index
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^code/', include('user_code.urls', namespace="user_code")),
    url(r'^login/$', log_in),
    url(r'^register/$', register),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
