from django.contrib import admin
from django.urls import path
from .views import register_user, login_view, home_view, logout_view, profile_view

urlpatterns = [
    path('register/', register_user, name = 'register'),
    path('login/', login_view, name = 'login'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),

]
