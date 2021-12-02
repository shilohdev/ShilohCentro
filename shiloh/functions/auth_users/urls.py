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
    path('api/manage/cadastrar/user/', views.ApiCadastreUser, name='ApiCadastreUser'),

    #CADASTRAR PARCEIROS
    path('api/manage/cadastrar/parceiros/', views.ApiCadastrePartners, name='ApiCadastrePartnes'),

    #CADASTRAR INDICAÇÃO
    path('cadastrar/indicacao/', views.cadastreIndicationViews, name='cadastreIndication'),

    #CADASTRAR INDICAÇÃO
    path('ApiCadastrar/indicacao/', views.ApiCadastreIndication, name='ApiCadastreIndication'),

    #API FORMATAR CPF
    path('API/CPF/', views.apiFormatCPF, name='apiFormatCPF'),
    
    #API FORMATAR CPF
    path('API/TEL/', views.apiFormatTEL, name='apiFormatTEL'),

    #CADASTRAR CONVENIO
    path('manage/cadastrar/convenio/', views.cadastreConvenioViews, name='cadastreConvenio'),

    #API CADASTRAR CONVENIO
    path('api/cadastre/convenio', views.ApiCadastreConvenio, name='ApiCadastreConvenio'),
    
    
    #API PERMISSOES USERS
    path('api/permissions/users', views.ApiPermissionsUsers, name='ApiPermissionsUsers'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)