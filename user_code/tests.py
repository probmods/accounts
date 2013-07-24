"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
import datetime
from django.contrib.auth import authenticate, login, get_user_model
from django.test.client import Client

from user_code.models import User_code, Exercise

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class User_codeViewTest(TestCase):
  
    def test_manually_post_code_exercise(self):
        count = Exercise.objects.count()
        e = Exercise(name='testing')
        e.save()
        new_count = Exercise.objects.count()
        self.assertEqual(count+1, new_count)
    
    # def test_post_code_exercise_exists(self):
    #         r = self.client.post('/login/', {'username': 'gamoeri@gmail.com', 'password': 'authsuperuser'})
    #         self.assertEqual(r.status_code, 200)
    #         e = Exercise(name='testing')
    #         e.save()
    #         count = Exercise.objects.count()
    #         self.assertEqual(count,1)
    #         resp = self.client.post('/code/testing', {'new_code': 'new exercise test'})
    #         self.assertEqual(resp.status_code, 301)
    #         new_count = Exercise.objects.count()
    #         code_count = User_code.objects.count()
    #         self.assertEqual(code_count,1)
    #         self.assertEqual(count, new_count)
    #         self.assertEqual(0,1)
    #     
    #     def test_post_code_exercise(self):
    #         r = self.client.post('/login/', {'username': 'gamoeri@gmail.com', 'password': 'authsuperuser'})
    #         self.assertEqual(r.status_code, 200)
    #         count = Exercise.objects.count()
    #         self.assertEqual(count,0)
    #         resp = self.client.post('/code/tester', {'new_code': 'new exercise test'})
    #         self.assertEqual(resp.status_code, 301)
    #         new_count = Exercise.objects.count()
    #         code_count = User_code.objects.count()
    #         self.assertEqual(code_count,1)
    #         self.assertEqual(count+1, new_count)
        
      