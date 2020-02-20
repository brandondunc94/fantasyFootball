import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm
from .models import User

def home(request):
    return render(request, 'home/index.html')

def login_request(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #Save off user email and password
            inputEmail = form.cleaned_data.get("email")
            inputPassword = form.cleaned_data.get("password")

            #Query for email and password combination
            user = User.objects.filter(email = inputEmail, password = inputPassword)
            
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
    
    return render(request, 'home/login.html', {'form': form})

def hello_there(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return HttpResponse(content)