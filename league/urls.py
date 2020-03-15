from league import views
from django.urls import path

urlpatterns = [
    path('create/', views.createLeague, name="New League"),
    path('join/', views.joinLeague, name="Join League"),
    path('home/', views.home, name="League Home"),
    path("home/<leagueName>/", views.home, name='League Home')
]