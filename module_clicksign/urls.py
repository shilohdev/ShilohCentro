from django.views.decorators.csrf import csrf_exempt
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from module_clicksign.views import (
    ModuleSendClickSign,
    WHookSendClickSign
)


urlpatterns = [ 
    # aPI ENVIAR DOCUMENTO CLICKSIGN // PARA TESTES
    path('api/clicksign/send/', ModuleSendClickSign.as_view(), name='ModuleSendClickSign'),
    path('whook/clicksign/', csrf_exempt(WHookSendClickSign.as_view()), name='WHookSendClickSign'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  