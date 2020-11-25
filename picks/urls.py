from django.urls import include, path
from picks import views

urlpatterns = [
    path('save/', views.save_pick, name='AJAX CALL - Save single pick'),
    path('compare/<homeTeamName>vs<awayTeamName>/', views.compare_teams, name='Compare two team stats'),
]