from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 

    path('api/anx/docs/patients/', views.ApiPathDocsPatientsViews, name='ApiPathDocsPatients'), #CRIAR DIRETORIO
    path('api/view/docs/patients', views.ApiListDocsPatientsViews, name='ApiListDocsPatients'), #LISTAR DOCS


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
