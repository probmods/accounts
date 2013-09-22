# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sessions.models import Session
from user_code.models import Code, Exercise, Result
from django.conf.urls import patterns, url
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from user_code.forms import ResultForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition

## TODO: etag is row id of resource
## we need to set and get this from memcache based on the user and exerciseName
def dummyetag(request, *args, **kwargs):
    return "blahx"

## TODO: last modified is the time of insertion into database
## we need to set and get this from memcache based on the user and exerciseName

#@condition(etag_func = dummyetag)
#@cache_page(60 * 60 * 24) # 60 seconds (1 minute) * 60 minutes (1 hour) * 24 hours (1 day)
def user_exercise(request, string):
    state = ''
    code = ''
    if request.method == 'POST':
        try:
            exercise = Exercise.objects.get(name=string)
        except Exercise.DoesNotExist:
            exercise = Exercise(name=string)
            exercise.save()
        
        new_code = Code(user_id = request.user,
                        exercise_id = exercise,
                        content = request.POST['code'],
                        engine = request.POST['engine'],
                        isRevert = request.POST['isRevert'],
                        isRerun = request.POST['isRerun'])
        
        new_code.save()
            # cache.set(string, request.POST['new_code'])
            # print cache.get(string)
        return redirect('/exercise/'+string)
    else: #GET 
        if request.user.is_authenticated(): 
          # code = cache.get(string)
          # cache.set(string, 'blah')
          # print string, cache.get(string), cache
          if not code:
            try:
               exercise = Exercise.objects.get(name=string)
               exists = True 
            except Exercise.DoesNotExist:
               return HttpResponseNotFound('page not found')
            if exists:
               user_exercise_code = Code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-date_created')[:1]
               if user_exercise_code.exists():
                  code = user_exercise_code[0].content
                  # cache.set(string, code)
               else:
                   return HttpResponseNotFound('page not found')
    return render(request, "code/exercise.html", {'code' : code})
    
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
    

def post_result(request):
    form = ResultForm()
    return render(request, "code/post_result.html", {'form': form})
    
def result(request):
    if request.method == 'POST' and request.user.is_authenticated():
        exercise_name = request.POST['exercise_id']
        try: 
          exercise = Exercise.objects.get(name=exercise_name)
          code = Code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-date_created')[:1]
          form = ResultForm(request.POST)
          result = form.save(commit=False)
          result.exercise_id = exercise
          result.user_id = request.user
          result.code_id = code[0]
          result.save()
        except Exercise.DoesNotExist:
          return HttpResponseNotFound('page not found')
        
    return render(request, "code/result.html")
  
