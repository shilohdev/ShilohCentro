from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),  
    path('', include('auth_users.urls')),
    path('', include('auth_patients.urls')),
    path('', include('auth_access.urls')),
    path('', include('module_clicksign.urls')),
    path('', include('auth_finances.urls')),
    path('', include('task_scheduling.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)