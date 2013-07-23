from django.db import models
from django.utils import timezone
import datetime
from django.conf import settings

# Create your models here.
    
class Exercise(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
        
class User_code(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    exercise_id = models.ForeignKey(Exercise) 
    content = models.TextField()
    date_created = models.DateTimeField('Date Saved')