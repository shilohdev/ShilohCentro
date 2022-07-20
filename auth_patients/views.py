from django.views import View
from django.db import connections
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import ensure_csrf_cookie
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from django.contrib import messages
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User 
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from datetime import datetime
from auth_patients.decorator import ApiPathDocsPatientsFunction, ApiListDocsPatientsFunction



#PATH DOCUMENTOS PRINCIPAIS DOS PACIENTES
@login_required
def ApiPathDocsPatientsViews(request):
    array = ApiPathDocsPatientsFunction(request)
    return JsonResponse(array, safe=False, status=200)

#LISTAS DOCS PRINCIPAIS DO PACIENTE
@login_required
def ApiListDocsPatientsViews(request):
    array = ApiListDocsPatientsFunction(request)
    return JsonResponse(array, safe=False, status=200)