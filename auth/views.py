from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.shortcuts import render, render_to_response, redirect
from custom_user.forms import EmailUserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from user_code.models import Exercise

def index(request):
	return render(request, 'auth/index.html')
	
def register(request):
    state = ''
    if request.method == 'POST':   # save user
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.is_active = True
            state = "Successfully created an account, please login"
            username = ''
            return render_to_response('auth/auth.html', {'state':state, 'username': username, 'form': AuthenticationForm()})
        else: 
            state = 'Sorry, there was an error processing your request'
    else:   #create user
        form = EmailUserCreationForm() 
    return render(request, "auth/register.html", {'form': form, 'state': state})

def log_in(request):
  if request.user.is_authenticated():
    return redirect('/home')
  else:
      state = "Please log in below..."  
      username = password = ''
      if request.POST: 
          form = AuthenticationForm(data=request.POST)
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password) 
          if user is not None:
              if user.is_active:
                  login(request, user)
                  state = "You're successfully logged in!"
                  return redirect('/home/')
              else:
                state = "Your account is not active, please contact the site admin."
          else:
              state = "Your username and/or password was incorrect."
      else:
          form = AuthenticationForm()
  return render(request, 'auth/auth.html', {'state': state, 'form' : form})

def home(request):
    if request.user.is_authenticated():
        return render(request, 'auth/home.html')
    else:
       return redirect('/login/')

def log_out(request):
    logout(request)
    return redirect('/')
    
def all_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, "auth/all_exercises.html", {'exercises' : exercises})
    
def each_exercise(request,string):
    state = ""
    exercise_name = "sorry, exercise doesn't exist"
    user = False
    if request.user.is_authenticated():
      user = True
    try:
        exercise = Exercise.objects.get(name=string)
        exercise_name = exercise.name
    except Exercise.DoesNotExist:
        state = "this exercise does not exist"
        return render(request, "auth/does_not_exist.html", {'state': state})
    return render(request, "auth/each_exercise.html", {'state': state, 'exercise_name' : exercise_name, 'auth_user':user})
      #get most recent code 
      #or post new code
  
  