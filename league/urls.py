from league import views
from django.urls import path

urlpatterns = [
    path('create/', views.createLeague, name="Create League"),
    path('join/', views.joinLeaguePage, name="Join League"),
    path('request/', views.requestLeague, name="AJAX - Request to join League"),
    path('addPrivate/', views.addUserToPrivateLeague, name="AJAX - Add user to Private League"),
    path('addPublic/', views.addUserToPublicLeague, name="AJAX - Add user to Public League"),
    path('post/', views.postLeagueMessage, name="AJAX - Post message to league board"),
    path('admin/<leagueName>/', views.leagueAdmin, name="League Admin page"),
]