# Football Fantasy
A new fantasy football based solely on picking game winners

#### Local Development Setup
  Use the following link for a nice guide: https://code.visualstudio.com/docs/python/tutorial-django

#### To add a new app
1. python manage.py startapp appname
2. Update fantasyFootball.urls.py to include urls of app
    Ex. url(r'^account/', include('account.urls')) where 'account' is the new app name

## NFL Logos Found at https://seeklogo.net/series/nfl-team-logos-vector

## How to Deploy
1. Navigate to server using putty, login with user and navigate to project folder.
  cd /home/bdunc/fantasyFootball
2. Git pull origin master
3. Start virtual env using: source env/bin/activate
4. If changes were made to static files, run: python manage.py collectstatic
  Make copy of all files/folders in 'static_root' to 'static' using: cp -a static_root/. static/
5. Exit virtual env with: deactivate
5. Restart Nginx and gunicorn using:  sudo systemctl restart nginx and sudo systemctl restart gunicorn

 ## Things to add
 1. Lock game pick automatically based on what day/time it currently is and what day/time the game is
 2. Admin locks individual games
 3. Add team records
 4. Enter all 2019-2020 game data
 5. User profile images?