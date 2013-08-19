# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sessions.models import Session
from user_code.models import Code, Exercise, Results
from django.conf.urls import patterns, url
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.core.cache import cache


@cache_page(60 * 60 * 24) # 60 seconds (1 minute) * 60 minutes (1 hour) * 24 hours (1 day)
def user_exercise(request, string):
    state = ''
    code = ''
    if request.method == 'POST':
        try:
            exercise = Exercise.objects.get(name=string)
        except Exercise.DoesNotExist:
            exercise = Exercise(name=string)
            exercise.save()
        if request.user.is_authenticated():
            new_code = Code(user_id = request.user, exercise_id = exercise, content = request.POST['new_code'])
            new_code.save()
            cache.delete(string)
        return redirect('/exercise/'+string)
    else: #GET 
        if request.user.is_authenticated():
          code = cache.get(string)
          if not code:
            try:
               exercise = Exercise.objects.get(name=string)
               exists = True 
            except Exercise.DoesNotExist:
               state = 'This exercise does not exist'
               return render(request, "accounts/does_not_exist.html", {'state': state})
            if exists:
               user_exercise_code = Code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-date_created')[:1]
               if user_exercise_code.exists():
                  code = user_exercise_code[0].content
                  cache.set(string, code)
               else:
                  state = "you do not have this exercise saved"     
    return render(request, "code/exercise.html", {'code' : code, 'state': state})
    
def view_all(request, string): 
    state = ''
    exists = False
    try:
       exercise = Exercise.objects.get(name=string)
       exists = True 
    except Exercise.DoesNotExist:
       state = 'exercise does not exist'
    if exists and request.user.is_authenticated():
       user_exercise_code = Code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-date_created')[:1]
       if not user_exercise_code.exists():
          code = user_exercise_code[0].content
       else:
          code = "you do not have this exercise saved"
    
    return render(request, "code/exercise.html", {'code' : code, 'state': state})