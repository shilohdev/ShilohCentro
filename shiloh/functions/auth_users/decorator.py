from django.db import connections
from django.db.models import query
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
import datetime
import base64
import json
import time
from re import A
from django.contrib.auth.models import User



#FUNCTION FORMATAR CPF
def formatcpfcnpj(cpf: str):
    if cpf in ["", None]:
       return ""

    return (((cpf.replace("-", "")).replace("/", "")).replace(".", "")).replace(" ", "")

    
#FUNCTION FORMATAR TELEFONE 
def formatTEL(tel: str):
    if tel in ["", None]:
       return ""

    return (((tel.replace("-", "")).replace("(", "")).replace(")", "")).replace(".", "")



def searchTPerfil(request):
    
    with connections['auth_permissions'].cursor() as cursor:
        #SELECT DO BANCO DIRETO PARA O SELECT HTML >>>> TIPO DE PERFFIL
        query = "SELECT id, descriptions FROM auth_permissions.permissions_type WHERE descriptions NOT LIKE  'Parceiro' ORDER BY descriptions;"
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

#CADASTRAR USER
def CadastreUser(request):
    tp_perfil = request.POST.get("tp_perfil")
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
    city = request.POST.get("city")
    uf = request.POST.get("uf")
    
    with connections['auth_users'].cursor() as cursor:
        #CADASTRAR PERFIL
        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")

        param =(cpf, name, date_nasc, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf,)
        query = "INSERT INTO `auth_users`.`users` (`id`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '', '', '', '');"
        cursor.execute(query, param)
        
        id_user = cursor.lastrowid

        param=(tp_perfil, id_user,)
        query = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id`, `id_permission`, `id_user`) VALUES (NULL, %s, %s);"
        cursor.execute(query, param)

        #AUTENTICAÇÃO E CRIAÇÃO DE LOGIN E SENHA    
        if User.objects.filter(username=cpf).exists():
            user = User.objects.get(username=cpf)
            user.nome = name
            user.email = email

            user.save()
        else:
            user = User.objects.create_user(username=cpf, email=email, first_name=name, last_name='', password=cpf)


    return {"response": "true", "message": "Cadastrado com sucesso!"}
    

#CADASTRAR PARCEIROS
def CadastrePartners(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    zipcode = request.POST.get("zipcode")
    addres = request.POST.get("addres")
    number = request.POST.get("number")
    complement = request.POST.get("complement")
    district = request.POST.get("district")
    city = request.POST.get("city")
    uf = request.POST.get("uf")
    obs = request.POST.get("obs")
    rn = request.POST.get("rn")
    categoria = request.POST.get("categoria")
    date = datetime.date.today()
    year = date.strftime("%Y")

    
    with connections['auth_users'].cursor() as cursor:
        #CADASTRAR PERFIL
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")

        param =(name, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, rn, categoria, obs, )
        query = "INSERT INTO `auth_users`.`users` (`id`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`) VALUES (NULL, '', %s, NULL,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '');"
        cursor.execute(query, param)

        id_user = cursor.lastrowid
        param=(id_user,)
        query = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id`, `id_permission`, `id_user`) VALUES (NULL, '7', %s);"
        cursor.execute(query, param)

            #AUTENTICAÇÃO E CRIAÇÃO DE LOGIN E SENHA    
        if User.objects.filter(username=rn).exists():
            user = User.objects.get(username=rn)
            user.nome = name
            user.email = email

            user.save()
        else:
            user = User.objects.create_user(username=rn, email=email, first_name=name, last_name='', password=year)
        
    return {"response": "true", "message": "Cadastrado com sucesso!"}


    #CADASTRAR INDICAÇÃO
def CadastreIndication(request):
    cpf = request.POST.get("cpf")
    name = request.POST.get("name")
    email = request.POST.get("email")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    obs = request.POST.get("obs")
    convenio = request.POST.get("obs")
    combo = request.POST.get("obs")

    
    with connections['customer_refer'].cursor() as cursor:
        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        param =(cpf, name, email, tel1, tel2, obs, convenio, combo, )
        query = "INSERT INTO `customer_refer`.`patients` (`id`, `cpf`, `nome`, `email`, `data_nasc`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `cidade`, `uf`, `convenio`, `exames`, `obs`) VALUES (NULL, %s, %s, %s, NULL , %s, %s, '' ,'' ,'' , '', '', '', '', %s, %s, %s);"
        cursor.execute(query, param)
        
    return {"response": "true", "message": "Cadastrado com sucesso!"}



#CADASTRAR CONVENIO
def cadastreConv(request):
    convenio = request.POST.get("convenio")
    
    with connections['customer_refer'].cursor() as cursor:

        param =(convenio,)
        query = "INSERT INTO `admins`.`health_insurance` (`id`, `nome_conv`, `status`) VALUES (NULL, %s, 'Ativo');"
        cursor.execute(query, param)
        
    return {"response": "true", "message": "Cadastrado com sucesso!"}


def searchCategoria(request):
    
    with connections['auth_permissions'].cursor() as cursor:
        #SELECT DO BANCO DIRETO PARA O SELECT HTML >>>> TIPO DE PERFFIL
        query = "SELECT * FROM auth_users.Category_pertners"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, categoria in dados:
            newinfoa = ({
                "categoria": categoria,
                "id": id
                })
            array.append(newinfoa)

        return array

  

