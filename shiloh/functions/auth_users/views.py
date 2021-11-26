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
from functions.auth_users.decorator import searchTPerfil, searchTPerfilExterno, CadastreUser
import base64
import json
import time
from re import A


def csrf_failure(request, reason=""):
    raise PermissionDenied()


#CADASTRAR USUARIO
def cadastreUserViews(request):
    searchPerfil = searchTPerfil(request)
    return render(request, 'manage/cadastre/cadastreUser.html', {"arr_SearchPerfil": searchPerfil})

    
#CADASTRAR PARCEIROS
def cadastrePartnesViews(request):
    searchPerfilEx = searchTPerfilExterno(request)
    return render(request, 'manage/cadastre/cadastrePartnes.html', {"arr_SearchPerfilEx": searchPerfilEx})


#API CADASTRAR PARCEIROS
def ApiCadastreUser(request):
    array = CadastreUser(request)
    return JsonResponse(array, safe=False, status=200)