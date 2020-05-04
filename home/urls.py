from django.urls import include, path
from home import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path("<int:weekId>/", views.dashboard, name='home'),
    path("<int:weekId>/<leagueName>/", views.dashboard, name='home'),
    path('welcome/', views.welcome, name='welcome')
]