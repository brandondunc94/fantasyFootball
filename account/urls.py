from django.urls import include, path
from account import views

urlpatterns = [
    path('', views.account_page, name='Account Home'),
    path('create/', views.create_account, name="New Account")
]