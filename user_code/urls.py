from django.conf.urls import patterns, url
from user_code import views
from user_code.views import user_exercise, all_user_exercise

urlpatterns = patterns('',
                       url(r'/_all$', all_user_exercise, name ='user_exercise'), 
                       url(r'/(?P<string>.+)$', user_exercise, name ='user_exercise'), 
)
