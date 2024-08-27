from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginform),
    path('home/', views.home, name='home'),
    path('accessInfo/', views.accessInfo, name='accessInfo'),
]