
from django.contrib import admin
from django.urls import path
from . import views
from .views import userLogin, suscripcion, userLogout, userRegistro, activar_cuenta

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('registro', views.registro, name='registro'),
    path('userLogin', userLogin, name='userLogin'),
    path('suscripcion', views.suscripcion, name='suscripcion'),
    path('logout', userLogout, name='logout'),
    path('userRegistro', userRegistro, name='userRegistro'),
    path('activar-cuenta/<int:user_id>/', views.activar_cuenta, name='activar_cuenta'),
]

 