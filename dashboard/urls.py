
from django.contrib import admin
from django.urls import path
from . import views
from .views import userLogin, suscripcion, userLogout, userRegistro, activar_cuenta, CustomChangePasswordView, dashboard_suscripcion

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('registro', views.registro, name='registro'),
    path('userLogin', userLogin, name='userLogin'),
    path('suscripcion', views.suscripcion, name='suscripcion'),
    path('logout', userLogout, name='logout'),
    path('userRegistro', userRegistro, name='userRegistro'),
    path('activar-cuenta/<int:user_id>/', views.activar_cuenta, name='activar_cuenta'),
    path('perfil', views.user_profile, name='perfil'),
    path('cambiaPass/', CustomChangePasswordView.as_view(), name='cambiaPass'),
    path('cambiaPass/logout', userLogout, name='cambiaPass/logout'),
    path('userLogout', userLogout, name='userLogout'),    
    path('dashboard_suscripcion', views.dashboard_suscripcion, name='dashboard_suscripcion'),

]

 