from django.urls import include, path
from account import views

urlpatterns = [
    path('', views.account, name='account'),
]