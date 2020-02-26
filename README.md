# Football Fantasy
A new fantasy football based solely on picking game winners

#### Local Development Setup
  Use the following link for a nice guide: https://code.visualstudio.com/docs/python/tutorial-django

####To add a new app
1. python manage.py startapp appname
2. Update fantasyFootball.urls.py to include urls of app
    Ex. url(r'^account/', include('account.urls')) whre 'account' is the new app name

##Logos Found at https://seeklogo.net/series/nfl-team-logos-vector