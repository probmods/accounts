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
from django.core.exceptions import PermissionDenied
from django.utils import simplejson

## TODO: etag is row id of resource
## we need to set and get this from memcache based on the user and exerciseName
def dummyetag(request, *args, **kwargs):
    return "blahx"

## TODO: last modified is the time of insertion into database
## we need to set and get this from memcache based on the user and exerciseName

def all_user_exercise(request):
    user = None
    if not request.user.is_authenticated():
        return HttpResponseNotFound('page not found')

    if not request.method == "GET":
        return HttpResponseNotFound('page not found')

    user = request.user

    ## eri named the foreign key objects poorly
    ## what should be "user_id" is actually "user"
    all_exercise_names = Code.objects.filter(user_id = user,
                                             exercise_id__name__contains="play-space").values("exercise_id__id", "exercise_id__name").distinct()

    ## HT http://stackoverflow.com/a/4424482/351392 and
    ## other answers on that page
    ## NB this can 
    all_exercise_names = list(all_exercise_names)
        
        
        
    #  print simplejson.dumps( all_exercise_names[0] )
   
    data = simplejson.dumps( all_exercise_names )
    return HttpResponse(data, mimetype = 'application/json')


#@condition(etag_func = dummyetag)
#@cache_page(60 * 60 * 24) # 60 seconds (1 minute) * 60 minutes (1 hour) * 24 hours (1 day)
def user_exercise(request, string):
    code = ''
    user = None
    if request.user.is_authenticated():
        user = request.user
    
    if request.method == 'POST':
        try:
            exercise = Exercise.objects.get(name=string)
        except Exercise.DoesNotExist:
            exercise = Exercise(name=string)
            exercise.save()
        
        new_code = Code(user_id = user,
                        exercise_id = exercise,
                        content = request.POST['code'],
                        engine = request.POST['engine'],
                        isRevert = request.POST['isRevert']
                        )
        if user == None:
            new_code.session_key = request.session.session_key
        
        new_code.save()
            # cache.set(string, request.POST['new_code'])
            # print cache.get(string)
        return HttpResponse(new_code.id)
    
    else: #GET 
        if request.user.is_authenticated(): 
          if not code:
            try:
               exercise = Exercise.objects.get(name=string)
               exists = True 
            except Exercise.DoesNotExist:
               return HttpResponseNotFound('page not found')
            if exists:
               user_exercise_code = Code.objects.filter(user_id=request.user, exercise_id= exercise).order_by('-id')[:1]
               if user_exercise_code.exists():
                  code = user_exercise_code[0].content
                  engine = user_exercise_code[0].engine
                  # cache.set(string, code) 
               else:
                   return HttpResponseNotFound('page not found')
          data = simplejson.dumps({'code': code, 'engine': engine})
          return HttpResponse(data, mimetype = 'application/json')
    return HttpResponseNotFound('page not found')
    
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
    if request.method == 'POST':
        user = None
        if request.user.is_authenticated():
            user = request.user
        exercise_name = request.POST['exercise_id']
        try: 
          exercise = Exercise.objects.get(name=exercise_name)
          code = Code.objects.get(id = request.POST['code_id'])

          form = ResultForm(request.POST)
          result = form.save(commit=False) 

          if user == None:
              # make sure the session is correct
              if (code.session_key != request.session.session_key):
                  raise PermissionDenied
              result.session_key = code.session_key
          else:
              # make sure this user has access to this code
              if (code.user_id.id != user.id):
                  raise PermissionDenied
          
          result.exercise_id = exercise
          result.user_id = user
          result.code_id = code
          result.save()
        except Exercise.DoesNotExist:
          return HttpResponseNotFound('page not found')
        
    return render(request, "code/result.html")
