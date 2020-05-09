from league import views
from django.urls import path
from command import views

urlpatterns = [
    path('', views.commandHome, name="Command Central with first season found"),
    path('createseason/', views.createSeason, name="Create new Season"),
    path('lock/', views.lockGame, name="AJAX - Lock picks for selected game"),
    path('unlock/', views.unlockGame, name="AJAX - Unlock picks for selected game"),
    path('addWeek/', views.addWeek, name="AJAX - Create new week for current selected season"),
    path('addGame/', views.addGame, name="AJAX - Create new game for current selected season"),
    path('deleteGame/', views.deleteGame, name="AJAX - Delete game"),
    path('saveScoreSpread/', views.saveScoreSpread, name="AJAX - Save game score and game spreads and score players"),
    path('<seasonYear>/', views.seasonSettings, name="Command Central with specific season"),
    path('<seasonYear>/<int:weekId>/', views.gameOptionsPage, name="Lock and score games"),
]