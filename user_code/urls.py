from django.conf.urls import patterns, url
from user_code import views
from user_code.views import user_exercise

urlpatterns = patterns('',
    url(r'/(?P<string>.+)$', user_exercise, name ='user_exercise'), 
)
