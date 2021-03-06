from league import views
from django.urls import path
from command import views

urlpatterns = [
    path('', views.commandHome, name="Command Central with first season found"),
    path('leaguemanage/', views.leagueManage, name="Manage Leagues"),
    path('leaguedelete/', views.deleteLeague, name="AJAX - Delete League"),
    path('lock/', views.lockGame, name="AJAX - Lock picks for selected game"),
    path('unlock/', views.unlockGame, name="AJAX - Unlock picks for selected game"),
    path('addWeek/', views.addWeek, name="AJAX - Create new week for current selected season"),
    path('addGame/', views.addGame, name="AJAX - Create new game for current selected season"),
    path('deleteGame/', views.deleteGame, name="AJAX - Delete game"),
    path('saveScoreSpread/', views.saveScoreSpread, name="AJAX - Save game score and game spreads and score players"),
    path('activateWeek/', views.activateWeek, name="AJAX - Save game score and game spreads and score players"),
    path('getWeekSchedule/', views.getUpcomingWeekSchedule, name="AJAX - Make a call to the API and store/update upcoming schedule."),
    path('getLatestScores/', views.getLiveScores, name="AJAX - Make a call to the API and store in progress game scores."),
    path('getFinalScores/', views.getFinalScores, name="AJAX - Make a call to the API and store final scores."),
    path('<seasonYear>/', views.seasonSettings, name="Command Central with specific season"),
    path('<seasonYear>/games/', views.gameOptionsPage, name="Lock and score games"),
    path('<seasonYear>/games/<int:weekId>/', views.gameOptionsPage, name="Lock and score games"),
]