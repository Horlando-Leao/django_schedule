"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from core import views as core_views
from django.views.generic import RedirectView


urlsadmin = [
    path('admin/', admin.site.urls),
]

urlslogin = [
    path('login/', core_views.login_user),
    path('login/submit', core_views.submit_login),
    path('logout/', core_views.logout_user),
]

urlsagenda = [
    path('', RedirectView.as_view(url='agenda/')),
    path('agenda/', core_views.lista_eventos),

    path('agenda/evento/', core_views.evento),
    path('agenda/evento/submit', core_views.submit_evento),
    path('agenda/evento/delete/<int:id_evento>/', core_views.delete_evento)
]

urlpatterns = [] 
urlpatterns.extend(urlsadmin)
urlpatterns.extend(urlslogin)
urlpatterns.extend(urlsagenda)
