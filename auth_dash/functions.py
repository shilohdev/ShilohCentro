from asyncio import exceptions
from email.policy import default
from multiprocessing.sharedctypes import Array
import numbers
from django.db import connections
from django.db.models import query
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, request
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
from django.contrib.auth.models import User
from numpy import empty
from pymysql import NULL
from functions.connection.models import Connection, Exams, RegisterActions
from django.forms import model_to_dict
from django.conf import settings
from django.core.files.storage import default_storage
import re

 

def PhotoRankFunction(request):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT b.id, a.resp_atendimento FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users b ON a.resp_atendimento = b.nome WHERE DATE(a.data_agendamento) = CURRENT_DATE() AND a.status = 'Concluído' GROUP BY a.resp_atendimento, b.id;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:
            for id, nome in dados:             
                newinfoa = ({
                    "id": id,
                    "nome": nome,                  
                    })                
                array.append(newinfoa)
            return array

        try:
            keysLIST = []
            id = ID
            PATH = settings.BASE_DIR_DOCS + f"/FotoPerfil/{id}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
            PATH_ORIGIN = f"/FotoPerfil/{id}"
            DS = default_storage #objeto
            if DS.exists(PATH): #se o o bjeto existe
                LIST_TYPES = DS.listdir(PATH) #lista tudo que esta dentro do meu objeto (pasta)
                if LIST_TYPES:
                    a = len(LIST_TYPES) > 0
                    if a:
                        for paths in LIST_TYPES[1]: #aqui pego o nome do arquivo
                                keysLIST.append({
                                    "url": settings.SHORT_PLATAFORM + f"/docs/FotoPerfil/{id}/{paths}"
                                })
            return keysLIST
            
        except Exception as err:
            print("ERRO:", err)
            return {
                "response": False,
                "message": "Não foi possível encontrar este usuário."
            }

def PhotoRankByArrayFunction(data):
    from auth_dash.models import PhotoServices
    
    PHOTO_SERVICES = PhotoServices()
    arr_response = {}
    if data:
        for key in data:
            id = str(key.get('id'))
            
            msg = PHOTO_SERVICES._get_photo_perfil(id)
            arr_response[id] = msg.get('message') if msg.get('response', None) else ""
    else: 
        arr_response = 0
    
    return arr_response
 



 
#RANKING DASHBOARD ATENDIMENTO > MÊS

def DashCollectionPendenteDiaFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT COUNT(status) AS qtd_pend, status FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURRENT_DATE() AND status = 'Pendente';"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        for qtd_pendente, status in dados:
            if qtd_pendente == 0:
                status = "Pendente"
            newinfoa = ({
                "qtd": qtd_pendente,
                "status": status,                
                })                
            array.append(newinfoa)
        return array

def DashCollectioAndamentoDiaFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT COUNT(status) AS qtd_pend, status FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURRENT_DATE() AND status = 'Em Andamento';"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        for qtd_pendente, status in dados:
            if qtd_pendente == 0:
                status = "Em Andamento"
                newinfoa = ({
                    "qtd": qtd_pendente,
                    "status": status,                
                    })                
                array.append(newinfoa)
        return array

def DashCollectionConcluidoDiaFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT COUNT(status) AS qtd_pend, status FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURRENT_DATE() AND status = 'Concluído';"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        for qtd_pendente, status in dados:
            if qtd_pendente == 0:
                status = "Concluído"
            newinfoa = ({
                "qtd": qtd_pendente,
                "status": status,                
                })                
            array.append(newinfoa)
        return array



def DashCollectionPendenteMesFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT count(status) AS qtd_mestotal, status FROM auth_agenda.collection_schedule WHERE Month(data_agendamento) = Month(CURRENT_DATE()) AND status = 'Pendente';"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        for qtd_pendente, status in dados:
            if qtd_pendente == 0:
                status = "Pendente"
            newinfoa = ({
                "qtd": qtd_pendente,
                "status": status,                
                })                
            array.append(newinfoa)
        return array

def DashCollectioAndamentoMesFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT count(status) AS qtd_mestotal, status FROM auth_agenda.collection_schedule WHERE Month(data_agendamento) = Month(CURRENT_DATE()) AND status = 'Em Andamento';"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        for qtd_pendente, status in dados:
            if qtd_pendente == 0:
                status = "Em Andamento"
            newinfoa = ({
                "qtd": qtd_pendente,
                "status": status,                
                })                
            array.append(newinfoa)
        return array

def DashCollectionConcluidoMesFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT count(status) AS qtd_mestotal, status FROM auth_agenda.collection_schedule WHERE Month(data_agendamento) = Month(CURRENT_DATE()) AND status = 'Concluído';"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        for qtd_pendente, status in dados:
            if qtd_pendente == 0:
                status = "Concluído"
            newinfoa = ({
                "qtd": qtd_pendente,
                "status": status,                
                })                
            array.append(newinfoa)
        return array




#CONTAGEM DASHBOARD COMERCIAL > DIA
def DashCommerceDayFunction(request):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT count(perfil) AS qtd_day FROM auth_users.users WHERE DATE(data_regis) = CURRENT_DATE() AND perfil = '7';"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
        for qtd_day in dados:
            if qtd_day == 0: 
                qtd_day = '0'
            else:
                qtd_day = int(qtd_day[0])
                newinfoa = ({
                    "qtd_day": qtd_day
                    })
                array.append(newinfoa)
        return array

#CONTAGEM DASHBOARD COMERCIAL > MÊS
def DashCommerceMonthFunction(request): 
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT count(perfil) AS qtd_mes FROM auth_users.users WHERE Month(data_regis) = Month(CURRENT_DATE()) AND perfil = '7';"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
        for qtd_mes in dados:
            if qtd_mes == 0: 
                qtd_mes = '0'
            else:
                qtd_mes = int(qtd_mes[0])        
                newinfoa = ({
                    "qtd_month": qtd_mes
                    })
                array.append(newinfoa)
    return array


#CONTAGEM DASHBOARD COMERCIAL > TOTAL
def CountDashTotalFunction(request):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT count(id) AS parc_total FROM auth_users.users WHERE perfil = '7';"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
        for qtd_all in dados:
            if qtd_all == 0:
                qtd_all = "0"
            else:
                qtd_all = int(qtd_all[0])
                newinfoa = ({
                    "qtd_all": qtd_all
                    })
                array.append(newinfoa)
        return array