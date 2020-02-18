from django.urls import path
from fantasyFootball import views

urlpatterns = [
    path("", views.home, name="home"),
]
