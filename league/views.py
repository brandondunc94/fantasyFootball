from django.shortcuts import render
from django.shortcuts import redirect
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
            return redirect('home')
    elif request.method == "GET":
            form = NewLeagueForm()
            return render(request, 'league/createLeague.html', {'form': form})

def joinLeague(request):
    if request.method == "POST":
        #Get league name from POST request
        leagueName = request.POST.get("league", "")

        #Get league object from DB
        league = League.objects.get(name=leagueName)
        
        #Join current user to the league
        leagueMembership = LeagueMembership.objects.create(user=request.user,league=league)

        return redirect('home')
    if request.method == "GET":
        #Query for leagues and render on page
        leagues = League.objects.all()
        return render(request, 'league/joinLeague.html', {'leagues': leagues})
