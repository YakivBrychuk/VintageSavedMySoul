# Description: This file contains the URL patterns for the home app.
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about_page, name='about'),
]
