from django.urls import include, path
from picks import views

urlpatterns = [
    path('', views.picks, name='Picks Home'),
    path("<int:weekId>/", views.picks, name='Picks Home with week'),
    path('save/', views.save_pick, name='AJAX CALL - Save single pick'),
]