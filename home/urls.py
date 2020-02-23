from django.urls import include, path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    #path(r'^home/', views.home, name='home'),
]