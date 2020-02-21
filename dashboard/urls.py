from django.urls import include, path
from dashboard import views

urlpatterns = [
    path('', views.home, name='home'),
    path('standings/', views.standings, name='standings'),
]