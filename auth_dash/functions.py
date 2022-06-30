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
from functions.general.decorator import convertDate, checkDayMonth, fetchQueryDashUnity
from django.forms import model_to_dict
from django.conf import settings
from django.core.files.storage import default_storage
import re



def RankingDashAtenDayFunction(request):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT b.id, a.resp_atendimento, COUNT(a.status) AS qtd_day FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users b ON a.resp_atendimento = b.nome WHERE DATE(a.data_agendamento) = CURRENT_DATE() AND a.status = 'Concluído' GROUP BY a.resp_atendimento, b.id ORDER BY qtd_day DESC LIMIT 10;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:
            for id, resp_atendimento, qtd_day in dados:
                nomes = resp_atendimento.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2              
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "qtd_day": qtd_day                    
                    })                
                array.append(newinfoa)
                
                PhotoRankFunction(id)

            return array


def PhotoRankFunction(ID):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT b.id, a.resp_atendimento, COUNT(a.status) AS qtd_day FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users b ON a.resp_atendimento = b.nome WHERE DATE(a.data_agendamento) = CURRENT_DATE() AND a.status = 'Concluído' GROUP BY a.resp_atendimento, b.id ORDER BY qtd_day DESC LIMIT 10;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:
            for id, resp_atendimento, qtd_day in dados:
                nomes = resp_atendimento.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2              
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "qtd_day": qtd_day                    
                    })                
                array.append(newinfoa)
                
                PhotoRankFunction(id)

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
