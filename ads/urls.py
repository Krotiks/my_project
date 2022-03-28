from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'ads'
urlpatterns = [
    path('', views.all_ads, name='all_ads'),
    path('<int:yy>/<int:mm>/<int:dd>/<slug:slug>', views.detailed_ad, name='detailed_ad'),
]