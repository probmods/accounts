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
from accounts.models import PmcUser
from accounts.forms import PmcUserCreationForm, PmcUserChangeForm

def index(request):
	return render(request, 'accounts/index.html')
	
def register(request):
    state = ''
    if request.method == 'POST':   # save user
        form = PmcUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.is_active = True
            state = "Successfully created an account, please login"
            new_user = authenticate(username=request.POST['email'], password=request.POST['password1']  )
            login(request, new_user)
            response = redirect("home")
            response.set_cookie('gg', 2)
            return response
        else: 
            state = 'Sorry, there was an error processing your request'
    else:   #create user
        form = PmcUserCreationForm()
    return render(request, "accounts/register.html", {'form': form, 'state': state})

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
                  response = redirect('home')
                  response.set_cookie('gg','1')
                  return response
              else:
                state = "Your account is not active, please contact the site admin."
          else:
              state = "Your username and/or password was incorrect."
      else:
          form = AuthenticationForm()
  return render(request, 'accounts/auth.html', {'state': state, 'form' : form})

def home(request):
    if request.user.is_authenticated():
        return render(request, 'accounts/home.html')
    else:
       return redirect('log_in')

def log_out(request):
    logout(request)
    response = redirect('index')
    response.delete_cookie('gg')
    return response
    
def all_exercises(request):
    exercises = Exercise.objects.all()
    return render(request, "accounts/all_exercises.html", {'exercises' : exercises})
    
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
        return render(request, "accounts/does_not_exist.html", {'state': state})
    return render(request, "accounts/each_exercise.html", {'state': state, 'exercise_name' : exercise_name, 'auth_user':user})
      #get most recent code 
      #or post new code
  

def profile(request):
    form = PmcUserChangeForm()
    return render(request, 'accounts/profile.html', {'form': form})
