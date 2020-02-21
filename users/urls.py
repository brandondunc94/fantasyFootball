from django.urls import path
from users import views

urlpatterns = [
    path("", views.home),
    path("login/", views.login_request, name="Login"),
    path("newUser/", views.create_user, name="Create User")
]