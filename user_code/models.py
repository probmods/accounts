from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings

# Create your models here.
    
class Exercise(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
        
class Code(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    exercise_id = models.ForeignKey(Exercise) 
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    engine = models.CharField(max_length = 50, default = 'webchurch')
    isRevert = models.BooleanField(default = False)
    isRerun = models.BooleanField(default = False)
    def __unicode__(self):
        return "Exercise: " +self.exercise_id.name + "    Content: " + self.content + "    User: " + self.user_id.email
        
class Result(models.Model):
    code_id = models.ForeignKey(Code)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    exercise_id = models.ForeignKey(Exercise)
    forest_errors = models.TextField(blank = True)
    forest_plots = models.TextField(blank = True)
    forest_results = models.TextField(blank = True)
    date_saved = models.DateTimeField(auto_now_add=True)
