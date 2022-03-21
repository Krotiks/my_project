from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'ads'
urlpatterns = [
    path('', views.all_ads, name='all_ads'),
]