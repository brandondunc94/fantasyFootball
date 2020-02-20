from django.urls import path
from home import views

urlpatterns = [
    path("", views.home),
    path("login/", views.login_request, name="login"),
]