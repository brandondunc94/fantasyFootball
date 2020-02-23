from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
@login_required
def home(request):
    #Get all leagues and display current stats based on picks

    #Get live scores and display on the top
    return render(request, 'home/home.html')