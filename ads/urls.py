from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ads'
urlpatterns = [
    #path('', views.all_ads, name='all_ads')
    path('', views.AdListView.as_view(), name='all_ads'),
    path('<int:yy>/<int:mm>/<int:dd>/<slug:slug>/',
         views.detailed_ad, name='detailed_ad'),
    path('<int:ad_id>/share/',
         views.share_ad, name='share_ad'),
    path('create/', views.create_ad, name='create_form'),
    #path('login/', views.custom_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
