from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    #CADASTRAR USUARIO
    path('manage/cadastrar/usuarios/', views.cadastreUserViews, name='cadastreUser'),
    #CADASTRAR PARCEIROS
    path('manage/cadastrar/parceiros/', views.cadastrePartnesViews, name='cadastrePartnes'),
    #API CADASTRAR USER
    path('api/manage/cadastrar/user/', views.ApiCadastreUser, name='CadastreUser'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)