"""fantasyFootball URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from account.views import login_redirect

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^command/', include('command.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^welcome/', include('home.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^league/', include('league.urls')),
    url(r'^picks/', include('picks.urls')),
    path('', login_redirect, name='login'),
]

urlpatterns += staticfiles_urlpatterns()
