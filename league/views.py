from django.shortcuts import render
from django.contrib.auth.models import User
from league.forms import NewLeagueForm
from league.models import League, LeagueMembership
from account.models import Profile

# Create your views here.
def createLeague(request):
    if request.method == "POST":
        form = NewLeagueForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])

            #Create new league model in db
            newLeague = League.objects.create(name=form.cleaned_data['name'])

            #Assign current user to new league - FIX THIS
            leagueMembership = LeagueMembership.objects.create(user=request.user,league=newLeague)
            #Return to home page
            return render(request, 'home/home.html')
    elif request.method == "GET":
            form = NewLeagueForm()
            return render(request, 'league/createLeague.html', {'form': form})