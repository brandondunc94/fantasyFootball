from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from league.forms import NewLeagueForm
from league import utils as leagueUtils
from league.models import League, LeagueMembership, LeagueMessage, LeagueMembershipRequest, LeagueNotification
from account.models import Profile
from django.http import JsonResponse

@login_required
def createLeague(request):
    if request.method == "POST":
        form = NewLeagueForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            #Check to see if this league name already exists
            existingLeague = League.objects.filter(name=form.cleaned_data['name'])
            if existingLeague:
                form = NewLeagueForm()
                return render(request, 'league/createLeague.html', {'form': form, 'error': 'The League name you entered has already been taken. Please try another League name.'})
            
            #Determine if league is public or private
            if form.cleaned_data['visibility'] == "Private":
                leagueIsPublic = False
            else:
                leagueIsPublic = True

            #Create new league model in db
            newLeague = League.objects.create(name=form.cleaned_data['name'], admin=request.user, description=form.cleaned_data['description'], isPublic=leagueIsPublic)

            #Assign current user to new league
            leagueMembership = LeagueMembership.objects.create(user=request.user,league=newLeague)
            
            #Set newLeague to active league for current user - THIS IS VERY IMPORTANT
            leagueUtils.setUserActiveLeague(request.user, newLeague)

            #Create welcome messages for league
            welcomeMessage = 'Welcome to your new league on OnsidePick! ' + request.user.username + ' is the administrator of your league.'
            infoMessage = 'Once games are available, begin making your picks and bets for upcoming games. You have been given 500 points to start which you may use to place bets on the spread of any game you choose. Game choices will lock 1 hour prior to kickoff, so be sure that you have submitted your picks and bets by then. Good luck!'
            leagueUtils.createLeagueNotification(newLeague.name, welcomeMessage)
            leagueUtils.createLeagueNotification(newLeague.name, infoMessage)

            #Return to home page
            return redirect('home')
            
    elif request.method == "GET":
            form = NewLeagueForm()
            return render(request, 'league/createLeague.html', {'form': form})

@login_required
def joinLeaguePage(request):
    #Query for leagues and render on page
    leagues = League.objects.exclude(members__username__iexact=request.user.username)
    leagueData = []
    for currentLeague in leagues:
        #Query to see if the user has already requested to join the current league
        pendingRequest = LeagueMembershipRequest.objects.filter(user=request.user, league=currentLeague)
        if pendingRequest:
            leagueData.append(
            {
                'pendingRequest': True,
                'league': currentLeague
            })
        else:
            leagueData.append(
            {
                'pendingRequest': False,
                'league': currentLeague
            })
    return render(request, 'league/joinLeague.html', {'leagueData': leagueData})

#AJAX CALL
@login_required
def requestLeague(request):
    leagueName = request.GET.get('leagueName', None)
    try:
        selectedLeague = League.objects.get(name=leagueName)
        #Make sure the user is not already part of this league
        try:
            leagueMember = LeagueMembership.objects.get(user=request.user,league=selectedLeague)
            if leagueMember:
                #User is already a member, send back status
                status = 'DUPLICATE'
        except:
            #Create request to join the league
            membershipRequest = LeagueMembershipRequest.objects.create(user=request.user,league=selectedLeague)
            status = 'SUCCESS'
    except:
        status = 'FAILED'
    
    data = {
            'status': status
        }

    return JsonResponse(data)

#AJAX CALL
@login_required
def addUserToPrivateLeague(request):
    leagueName = request.GET.get('leagueName', None)
    username = request.GET.get('username', None)

    #Make sure current user is the admin of the league
    try:
        leagueAdmin = League.objects.get(admin=request.user, name=leagueName)
    except:
        return redirect('/league/home/')

    #Make sure user is not already in this league
    #INSERT LOGIC HERE

    #Get user from username passed in
    requestedUser = User.objects.get(username=username)
    try:
        #Create new league membership object
        newMembership = LeagueMembership.objects.create(league=leagueAdmin, user=requestedUser)

        #Set newly joined league to active league for requested user
        leagueUtils.setUserActiveLeague(requestedUser, leagueAdmin)
        status = 'SUCCESS'
        #Delete request to join league
        try:
            leagueRequest = LeagueMembershipRequest.objects.get(user=requestedUser, league=leagueAdmin)
            leagueRequest.delete()
        except:
            status = 'PARTIAL'
            print("Error - Could not delete league membership request.")
        
        #Add new league update to show new user joined
        leagueUtils.createLeagueNotification(leagueAdmin.name, requestedUser.username + " has joined the league!")

    except:
        status = 'FAILED'
        print("Error - could not add user to the league.")

    data = {
            'status': status
        }
    
    return JsonResponse(data)

#AJAX CALL
@login_required
def addUserToPublicLeague(request):
    leagueName = request.GET.get('leagueName', None)

    #Get league object
    try:
        league = League.objects.get(name=leagueName)
        #Make sure user is not already in this league
        try:
            existingMember = LeagueMembership.objects.get(user=request.user, league=league)
            #If found, set status to 'DUPLICATE' and return
            status = 'DUPLICATE'
        except:
            try:
                #Create new league membership object
                newMembership = LeagueMembership.objects.create(league=league, user=request.user)

                #Set newly joined league to active league for requested user
                leagueUtils.setUserActiveLeague(request.user, league)
                status = 'SUCCESS'

            except:
                status = 'FAILED'
                print("Error - could not add user to the league.")
        
        #Add new league update to show new user joined
        leagueUtils.createLeagueNotification(leagueName, request.user.username + " has joined the league!")
    except:
        status = 'FAILED'

    data = {
            'status': status
        }
    
    return JsonResponse(data)

#AJAX CALL
def postLeagueMessage(request):
    #Log message
    newMessage = request.POST.get("message", "")
     
    if not newMessage:
        return render(request, 'league/leagueHome.html')
    else:
        #Get active league
        activeLeague = Profile.objects.get(user=request.user).currentActiveLeague
        #activeLeague = League.objects.get(name=activeLeagueName)

        newLeagueMessage = LeagueMessage.objects.create(user=request.user, league=activeLeague, message=newMessage)
        newLeagueMessage.save()
        status = 'SUCCESS'
        data = {
            'status': status
        }
        
        return JsonResponse(data)

@login_required
def leagueAdmin(request, leagueName=""):
    
    if leagueName:
        try:
            #Check to see if current user is an admin
            activeLeague = League.objects.get(name=leagueName, admin=request.user)
        except:
            #User is not an admin or the league does not exist
            return redirect("/home/")
    else:
        #League name not passed in, redirect to home page
        return redirect("/home/")

    #Get league users
    leagueUsers = LeagueMembership.objects.filter(league=activeLeague)

    #Get leagueRequests
    leagueRequests = LeagueMembershipRequest.objects.filter(league=activeLeague)
    return render(request, 'league/leagueSettings.html', {'leagueUsers': leagueUsers, 'leagueRequests': leagueRequests, 'activeLeague': activeLeague})

