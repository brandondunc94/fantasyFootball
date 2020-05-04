# Football Fantasy
A new fantasy football based solely on picking game winners

#### Local Development Setup
  Use the following link for a nice guide: https://code.visualstudio.com/docs/python/tutorial-django

#### To add a new app
1. python manage.py startapp appname
2. Update fantasyFootball.urls.py to include urls of app
    Ex. url(r'^account/', include('account.urls')) where 'account' is the new app name

## NFL Logos Found at https://seeklogo.net/series/nfl-team-logos-vector

## Color Scheme
Green: #19A404
Grey: #3A506B
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
1. Enter into postgres with: 'su - postgres' then 'psql'
2. 'DROP DATABASE dbname;' If there are live connections, kill them with
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = 'dbname'
    AND pid <> pg_backend_pid();
3. 'CREATE DATABASE dbname;'
4. 'GRANT ALL PRIVILEGES ON DATABASE dbname TO db_user;' '\q' to quit
5. If changes to models - Start virtual env using: 'source env/bin/activate'
6. Then run 'python manage.py migrate'

 # Celery (Without supervisor)
 1. Start the worker INSIDE THE VIRTUAL ENV with 'celery -A fantasyFootball worker --loglevel=info'
 2. Start celery beat with 'celery -A fantasyFootball beat'

 # Celery (With supervisor)
 1. 

 ## Things to add
 1. Add betting on game spread using points
 2. Add ability to edit games and add new games/weeks/seasons
 3. Enforce strong password when creating account
 4. Clean up pick page, beautify UI like the betting page
 5. User profile images
 6. Make default home page when season is not active

League selection in nav bar with join league and create league

Change 'home' to 'dashboard'

Dashboard Picks Bets

Make league home contents in dashboard