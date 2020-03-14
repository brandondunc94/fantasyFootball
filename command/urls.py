from league import views
from django.urls import path
from command import views

urlpatterns = [
    path('', views.command, name="Command Central"),
    path('createseason/', views.createSeason, name="Create new Season"),
    path('score/<int:weekId>/', views.scoreWeek, name="Count up scores for given week"),
    path("lock/<int:weekId>/", views.lockWeek, name='Lock picks for upcoming week'),
]