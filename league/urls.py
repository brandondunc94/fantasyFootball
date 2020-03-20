from league import views
from django.urls import path

urlpatterns = [
    path('create/', views.createLeague, name="New League"),
    path('join/', views.joinLeaguePage, name="Join League"),
    path('request/', views.requestLeague, name="AJAX - Request to join League"),
    path('home/', views.home, name="League Home"),
    path("home/<leagueName>/", views.home, name='League Home'),
    path("admin/<leagueName>/", views.leagueAdmin, name='League Home'),
    path('add/<username>/<leagueName>/', views.addToLeague, name="Add to league League")
]