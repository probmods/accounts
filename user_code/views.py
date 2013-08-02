# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sessions.models import Session
from user_code.models import User_code, Exercise
from django.conf.urls import patterns, url
from django.utils import timezone


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
            new_code = User_code(user_id = request.user, exercise_id = exercise, content = request.POST['new_code'])
            new_code.save()
        return redirect('/exercise/'+string+'/')
    else: #GET 
        exists = False
        try:
           exercise = Exercise.objects.get(name=string)
           exists = True 
        except Exercise.DoesNotExist:
           state = 'This exercise does not exist'
           return render(request, "auth/does_not_exist.html", {'state': state})
        if exists and request.user.is_authenticated():
           user_exercise_code = User_code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-date_created')[:1]
           if user_exercise_code.exists():
              code = user_exercise_code[0].content
           else:
              code = "you do not have this exercise saved"   
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
       user_exercise_code = User_code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-date_created')[:1]
       if not user_exercise_code.exists():
          code = user_exercise_code[0].content
       else:
          code = "you do not have this exercise saved"
    
    return render(request, "code/exercise.html", {'code' : code, 'state': state})