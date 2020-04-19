from league import views
from django.urls import path
from bets import views

urlpatterns = [
    path('', views.betsHome, name="Betting Homepage"),
]