# carousel/urls.py
from django.urls import path
from . import views

app_name = 'carousel'

urlpatterns = [
    path('<int:pk>/', views.carousel_home, name='carousel_home'),
    path('add/', views.add_familiar, name='add_familiar'),
    path('edit/<int:pk>/', views.edit_familiar, name='edit_familiar'),
    path('remove/<int:pk>/', views.remove_familiar, name='remove_familiar'),
    path('comments/', views.post_comment, name='post_comment'),
    path('comments/fetch/', views.fetch_comments, name='fetch_comments'),
]
