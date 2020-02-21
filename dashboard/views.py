from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def standings(request):
    return render(request, 'dashboard/standings.html')
