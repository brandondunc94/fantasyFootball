from django.urls import include, path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path("<int:weekId>/", views.home, name='home'),
    path("<int:weekId>/<leagueName>/", views.home, name='home'),
    path('welcome/', views.welcome, name='welcome')
]