from django.urls import include, path
from picks import views

urlpatterns = [
    path('', views.picks, name='Picks Home'),
    path("<int:weekId>/", views.picks, name='Picks Home'),
    path("<int:weekId>/<leagueName>/", views.picks, name='Picks Home')
]