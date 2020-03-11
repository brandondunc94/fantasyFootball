from league import views
from django.urls import path
from command import views

urlpatterns = [
    path('', views.command, name="Command Central"),
    path('score/', views.scorePlayers, name="Count up scores"),
    path('createseason/', views.createSeason, name="New Season")
]