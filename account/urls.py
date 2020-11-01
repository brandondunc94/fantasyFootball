from django.urls import include, path
from account import views

urlpatterns = [
    path('', views.account_page, name='Account Home'),
    path('create/', views.create_account, name='New Account'),
    path('delete/', views.delete_account, name='Delete Account'),
    path('lastAccess/', views.update_last_accessed_page, name='AJAX CALL - Update last accessed page'),
    path('update/', views.update_profile, name='AJAX CALL - Update profile when user clicks save'),
    path('<username>/',views.public_account_page, name='Public Account View'),
]