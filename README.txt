Accounts management in Django for the web book, Probabilistic Models of Cognition. This project provides:
- accounts for users
- saving and retrieving code for users


# Local installation

Set up virtualenv to install the requirements:

    virtualenv --python=/path/to/python env
    source env/bin/activate
    pip install -r requirements.txt

On OS X with MacPorts, the python path is likely to be `/opt/local/bin/python`. You'll want to run this with Python 2.7.

Next, initialize the database. First, inside `pmc/settings.py`, edit the INSTALLED_APPS variable: comment out everything except for `south`, all the `django.contrib` lines, and `custom_user`. Then, run `./manage.py syncdb`. Now, uncomment the lines in INSTALLED_APPS. Afterwards, for each app that you commented out, run:

    ./manage.py schemamigration APPNAME --initial

And then, for each app, run:

    ./manage.py migrate APPNAME

To update migrations, we use `./manage.py schemamigration APPNAME --auto` and `./manage.py migrate APPNAME`.

Currently, there are two apps in this project: `auth` and `user_code`.

Accounts:
------
Wraps all the functionality to manage user accounts. It also provides
a UI platform to view and save code.
It provides the view and template for the following urls: 
	- /register
	- /login
	- /logout
	- /home
	- /exercise/_all
	- /exercise/<exercise name>

/register, /login, /logout 
	These urls are for user authentication. After a user logs in,
	they are redirected to the /home page
    
/home 
	The /home/ page is the user's profile. If an unauthenticated user
	tries to access this page, it will redirect them to the login page. 
	It contains a link to /all_exercises/.
    
/exercise/_all
	Lists all the exercises currently present in the database. 
	The exercises correspond to each church code box on the website. Each
	exercise name is a link to the individual exercises' page.
	This page does not require user authentication.
	*** Currently, this page contains a textarea. When this page is submitted,
	the code in the textarea is saved as a instance of a user_code of a 
	hard coded exercise name. This tests the functionality of adding a new 
	exercise through the static html pages with javascript. 
/exercise/<exercise name>
	This page contains a link to the most recently saved exercise code and
	a textarea to save a new instance of an exercise code. 

# user_code
Takes care of the functionality of retrieving and saving exercise codes. 
It provides the view and template for this url:
- /code/<exercise_name>

`/code/<exercise_name>`

When the request is a GET request, it will serve a page back with the
most recently saved code for the user for the specific exercise. If the 
exercise does not exists, it will say so. Currently, if a user is
not authenticated, it will not do anything in the database.
When the request is a POST request, it will save the submitted text
with the user id and the exercise id. If the exercise name does not
exist, it will create the exercise and then save it, again with the 
user id and the exercise name (that now exists). If a user is not
authenticated, it will also do nothing. 
	

# Deployment: 
make sure that `custom_user` and `south` are added to the `INSTALLED_APPS` section of settings.py



