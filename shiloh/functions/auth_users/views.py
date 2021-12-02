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
from functions.auth_users.decorator import CadastreUser, CadastrePartners, CadastreIndication, formatcpfcnpj, formatTEL, cadastreConv
from functions.auth_users.decorator import searchTPerfil, searchCategoria
from functions.auth_users.decorator import allowPage
import base64
import json
import time
from re import A

def csrf_failure(request, reason=""):
    raise PermissionDenied()


#CADASTRAR USUARIO
def cadastreUserViews(request):
    searchPerfil = searchTPerfil(request)
    return render(request, 'manage/cadastre/Perfis/cadastreUser.html', {"arr_SearchPerfil": searchPerfil})

    
#CADASTRAR PARCEIROS
def cadastrePartnesViews(request):
    SsearchCategoria = searchCategoria(request)
    return render(request, 'manage/cadastre/Perfis/cadastrePartnes.html', {"arr_SearchCategoria": SsearchCategoria})


#API CADASTRAR USUARIOS
def ApiCadastreUser(request):
    array = CadastreUser(request)
    return JsonResponse(array, safe=False, status=200)

#API CADASTRAR PARCEIROS
def ApiCadastrePartners(request):
    array = CadastrePartners(request)
    return JsonResponse(array, safe=False, status=200)


#CADASTRAR INDICAÇÃO
def cadastreIndicationViews(request):
    return render(request, 'manage/cadastre/Perfis/cadastreIndication.html')

    
#API CADASTRAR INDICAÇÃO
def ApiCadastreIndication(request):
    array = CadastreIndication(request)
    return JsonResponse(array, safe=False, status=200)


#API FORMATAR CPF
def apiFormatCPF(request):
    array = formatcpfcnpj(request)
    return JsonResponse(array, safe=False, status=200)

    
#API FORMATAR NÚMERO DE TEL
def apiFormatTEL(request):
    array = formatTEL(request)
    return JsonResponse(array, safe=False, status=200)


#CADASTRAR CONVENIO
def cadastreConvenioViews(request):
    return render(request, 'manage/cadastre/Convenio/cadastreConvenio.html')

    
#API CADASTRAR CONVENIO
def ApiCadastreConvenio(request):
    array =  cadastreConv(request)
    return JsonResponse(array, safe=False, status=200)


#API PERMISSOES USERS
def ApiPermissionsUsers(request):
    array =  allowPage(request)
    return JsonResponse(array, safe=False, status=200)

