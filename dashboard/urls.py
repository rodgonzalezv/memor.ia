from django.contrib import admin
from django.urls import path
from . import views
from .views import CustomChangePasswordView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('list/', views.list_familiares, name='list_familiares'),
    path('add/', views.add_familiar, name='add_familiar'),
    path('update/<int:pk>/', views.update_familiar, name='update_familiar'),
    path('delete/<int:pk>/', views.delete_familiar, name='delete_familiar'),
    path('userLogout', views.userLogout, name='userLogout'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('cambiaPass', CustomChangePasswordView.as_view(), name='cambiaPass'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)