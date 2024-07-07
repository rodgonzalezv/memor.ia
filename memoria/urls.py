from django.urls import path
from . import views

app_name = 'memoria'  # Add this line

urlpatterns = [
    path('', views.home, name='home'),
    path('quienes_somos/', views.quienes_somos, name='quienes_somos'),
    path('planes/', views.planes, name='planes'),
    path('galeria/', views.galeria, name='galeria'),
    path('contacto/', views.contacto, name='contacto'),
    path('dashboard_home/', views.dashboard_home, name='dashboard_home'),
    path('dashboard_familiarRegistro/', views.familiarRegistro, name='dashboard_familiarRegistro'),
    path('dashboard_familiarListado/', views.familiarListado, name='dashboard_familiarListado'),
    path('familiarDelete/<int:familiar_id>/', views.familiarDelete, name='familiarDelete'),
    path('dashboard_familiarUpdate/<int:familiar_id>/', views.familiarUpdate, name='dashboard_familiarUpdate'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('userRegistro/', views.userRegistro, name='userRegistro'),
    path('activar-cuenta/<int:user_id>/', views.activar_cuenta, name='activar_cuenta'),
    path('cambiaPass/', views.CustomChangePasswordView.as_view(), name='cambiaPass'),
    path('cambiaPass/logout/', views.userLogout, name='cambiaPass/logout'),
    path('perfil/', views.user_profile, name='perfil'),
    path('dashboard_suscripcion/', views.dashboard_suscripcion, name='dashboard_suscripcion'),
    path('pagoexitoso/', views.pago_exitoso, name='pagoexitoso'),
    path('queplan/', views.queplan, name='queplan'),
]
