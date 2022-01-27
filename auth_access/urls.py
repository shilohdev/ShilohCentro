from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # PERMISSÕES
    path('manage/access/permissions/', views.setPermissionViews, name='setPermission'),
    path('api/permissions/save/', views.ApiSavePermissionsViews, name='ApiSavePermissions'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)