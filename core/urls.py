from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from memoria import views as memoria_views  # Import the views from memoria

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', memoria_views.home, name='home'),  # Set the home view as the default
    path('memoria/', include('memoria.urls', namespace='memoria')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('carousel/', include('carousel.urls', namespace='carousel')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
