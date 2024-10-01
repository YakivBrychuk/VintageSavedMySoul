# Description: This file contains the URL patterns for the home app.
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout')
]
