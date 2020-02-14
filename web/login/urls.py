from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='Login'),
    path('logout/', views.logout, name='logout'),
    path('404/', views.error404, name='404'),
    path('dashboard/', views.dashboard, name='Dashboard'),
    path('delete/', views.delete, name='Delete'),
    path('verify/', views.verifyOTP, name='verifyOTP')
]