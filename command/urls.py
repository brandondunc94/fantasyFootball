from league import views
from django.urls import path
from command import views

urlpatterns = [
    path('', views.commandHome, name="Command Central with first season found"),
    path('createseason/', views.createSeason, name="Create new Season"),
    path('lock/', views.lockGame, name="AJAX - Lock picks for selected game"),
    path('unlock/', views.unlockGame, name="AJAX - Unlock picks for selected game"),
    path('save-score/', views.saveScore, name="AJAX - Unlock picks for selected game"),
    path('<seasonYear>/', views.seasonSettings, name="Command Central with specific season"),
    path('<seasonYear>/<int:weekId>/', views.gameOptionsPage, name="Lock and score games"),
]