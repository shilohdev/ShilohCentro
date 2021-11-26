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
import base64
import json
import time
from re import A


def searchTPerfil(request):
    
    with connections['auth_permissions'].cursor() as cursor:
        #SELECT DO BANCO DIRETO PARA O SELECT HTML >>>> TIPO DE PERFFIL
        query = "SELECT id, descriptions FROM auth_permissions.permissions_type;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, descriptions in dados:
            newinfoa = ({
                "descriptions": descriptions,
                "id": id
                })
            array.append(newinfoa)

        return array


def searchTPerfilExterno(request):
    
    with connections['auth_permissions'].cursor() as cursor:
        #SELECT DO BANCO DIRETO PARA O SELECT HTML >>>> TIPO DE PERFFIL
        query = "SELECT id, descriptions FROM auth_permissions.permissions_type;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, descriptions in dados:
            array.append({
                "descriptions": descriptions,
                "id": id
                })

def CadastreUser(request):

    cpf = request.POST.get("cpf")
    name = request.POST.get("name")
    date_nasc = request.POST.get("date_nasc")
    email = request.POST.get("email")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    zipcode = request.POST.get("zipcode")
    addres = request.POST.get("addres")
    number = request.POST.get("number")
    complement = request.POST.get("complement")
    district = request.POST.get("district")
    uf = request.POST.get("uf")

    with connections['auth_permissions'].cursor() as cursor:
        #CADASTRAR PERFIL
        param =(cpf, name, date_nasc, email, tel1, tel2, zipcode, addres, number, complement, district, uf,)
        query = "INSERT INTO `auth_users`.`users` (`id`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `uf`, `cr`, `obs`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '');"
        cursor.execute(query, param)
    
    print(query)
    
