from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    #API MEU FINANCEIRO EM MASSA 
    path('teste/', views.teste, name='teste'),
    path('financeiro/solicitacoes/reembolso/', views.ReembolsoFinanceiro, name='ReembolsoFinanceiro'), #FINANCEIRO EXAMES


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  