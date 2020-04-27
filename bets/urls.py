from league import views
from django.urls import path
from bets import views

urlpatterns = [
    path('', views.betsHome, name="Betting Homepage"),
    path("<int:weekId>/", views.betsHome, name='Betting Homepage'),
    path("<int:weekId>/<leagueName>/", views.betsHome, name='Betting Homepage')
]