from django.shortcuts import render
from .forms import NewLeagueForm

# Create your views here.
def createLeague(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['username'])
            #Create new user using User model
            newUser = User.objects.create_user(form.cleaned_data['username'], 'bro_duncan18@yahoo.com'
                                                ,form.cleaned_data['password'])
            #Login newUser
            if newUser is not None:
                login(request, newUser)
                #Create new profile using Profile model and pass in newUser
                newProfile = Profile(user = newUser, bio = "I like football.", location = "Seattle")
                newProfile.save()
                return render(request, 'home/home.html')
    elif request.method == "GET":
            form = NewLeagueForm()
            return render(request, 'league/createLeague.html', {'form': form})