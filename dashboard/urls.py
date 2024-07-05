from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('list/', views.list_familiares, name='list_familiares'),
    path('add/', views.add_familiar, name='add_familiar'),
    path('update/<int:pk>/', views.update_familiar, name='update_familiar'),
    path('delete/<int:pk>/', views.delete_familiar, name='delete_familiar'),
]
