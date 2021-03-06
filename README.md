# Onside Pick
Created using the Django framework - A season long NFL competition where you compete in a league to earn the most points through picks and spread bets.

#### Local Development Setup
  Use the following link for a nice guide: https://code.visualstudio.com/docs/python/tutorial-django

#### To add a new app
1. python manage.py startapp appname
2. Update fantasyFootball.urls.py to include urls of app
    Ex. url(r'^account/', include('account.urls')) where 'account' is the new app name

## NFL Logos Found at https://seeklogo.net/series/nfl-team-logos-vector

## Color Scheme
Green: #19A404
Grey: #4d4b4b
White: #ffffff
Light Blue: #33A1FD
Medium Blue: #3066be
Dark Blue: #1B2A41

## How to Deploy
1. Navigate to server using putty, login with user bdunc and navigate to project folder.
  'cd /home/bdunc/fantasyFootball'
2. 'Git pull origin master' or 'git reset --hard origin/master'
3. Start virtual env using: 'source env/bin/activate'
4. If changes were made to static files, run: 'python manage.py collectstatic --noinput --clear'
5. Make copy of all files/folders in /static_in_env to /static using: 'cp -a static_in_env/. static/'
6. Exit virtual env with: 'deactivate'
7. Restart Nginx and gunicorn using:  'sudo systemctl restart nginx' and 'sudo systemctl restart gunicorn'

## Postgres commands
1. Enter into postgres with root user and type: 'su - postgres' then 'psql'
2. 'DROP DATABASE dbname;' If there are live connections, kill them with
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'dbname'
    AND pid <> pg_backend_pid();
3. 'CREATE DATABASE dbname;'
4. 'GRANT ALL PRIVILEGES ON DATABASE dbname TO db_user;' '\q' to quit
5. If changes to models - Start virtual env using: 'source env/bin/activate'
6. Then run 'python manage.py migrate'

#Spread payout logic
1. If user picked home team
    If home team was supposed to win by # points
      If the home team won by at least # points
        Pay player 90% of their bet (betAmount * 1.9)
      else
        Take player's bet amount and pay 0
    If home team was supposed to lost by # points
      If the home team lost by less than the spread
        Pay player 90% of their bet (betAmount * 1.9)
      else
        Take player's bet amount and pay 0
  If user picked away team
    If away team was supposed to win by # points
      If away team won by at least # points
        Pay player 90% of their bet (betAmount * 1.9)
      else
        Take player's bet amount and pay 0
    If away team was supposed to lost by # points
      If away team lost by at least # points
        Pay player 90% of their bet (betAmount * 1.9)
      else
        Take player's bet amount and pay 0

 # Celery (Without supervisor)
 1. Start the worker INSIDE THE VIRTUAL ENV with 'celery -A fantasyFootball worker --loglevel=info'
 2. Start celery beat with 'celery -A fantasyFootball beat'

 # Celery (With supervisor)
 1. supervisor stop celerybeat (as root)
 2. supervisor stop celeryworker
 3. supervisorctl reload
 
How Celery Works:
1. __init__.py uses celery.py to load in Celery app
2. celery.py initializes celery app with predefined settings located in settings.py

Adding a new scheduled task:
1. Add task to settings.py in CELERY_BEAT_SCHEDULE
2. Restart supervisor using 'supervisorctl reload' as root user

