from django.urls import path
from . import views

app_name = 'qr'

urlpatterns = [
    path('', views.generar_qr, name='generar_qr'),
]