from django.contrib import admin
from django.urls import path
from .views import hola_mundo, simple

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', simple),
]
