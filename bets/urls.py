from league import views
from django.urls import path
from bets import views

urlpatterns = [
    path('save/', views.save_bets, name="AJAX CALL - Save bets"),
]