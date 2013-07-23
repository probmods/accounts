# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sessions.models import Session
from user_code.models import User_code, Exercise

def user_exercise(request, string):
    state = 'default'
    if request.method == 'POST':
        state = 'method is POST'
        try:
            exercise = Exercise.objects.get(name=string)
        except Exercise.DoesNotExist:
            exercise = Exercise(name=string)
            exercise.save()
        new_code = User_code(user_id = request.user.id, exercise_id = exercise.id, date_created = timezone.now, content = '')
        new_code.save()
    else:
        state = 'method is GET'
        exercise = Exercise.objects.filter(name=string)
        code = ''
        # if request.user.is_authenticated():
        #           state += ' and is authenticated'
        if exercise.exists() and request.user.is_authenticated():
            exercise = Exercise.objects.get(name=string)
            user_exercise_code = User_code.objects.filter(user_id=request.user.id, exercise_id= exercise.id).order_by('-date_created')[:0]
            code = 'you do no have this exercise saved'
            if user_exercise_code.exists(): 
                code = user_exercise_code.content
    return render(request, "code/exercise.html", {'code' : code, 'state': state})
