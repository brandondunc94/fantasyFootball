from league import views
from django.urls import path

urlpatterns = [
    path('create/', views.createLeague, name="New League")
]