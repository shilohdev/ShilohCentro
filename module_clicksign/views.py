from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from functions.module_clicksign.decorator import ModuleSendClickSignFunction, WHookSendClickSignFunction

# Create your views here.
class ModuleSendClickSign(View):
    @staticmethod
    @csrf_exempt
    def get(request):
        return JsonResponse(
            ModuleSendClickSignFunction(request),
            status=200,
            safe=False
        )

class WHookSendClickSign(View):
    @classmethod
    def _callback(self, request):
        return JsonResponse(
            WHookSendClickSignFunction(request),
            status=200,
            safe=False
        )

    def post(self, request):
        return self._callback(request)

    def get(self, request):
        return self._callback(request)