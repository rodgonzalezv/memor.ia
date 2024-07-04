from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('dashboard/', include('dashboard.urls')),

]

