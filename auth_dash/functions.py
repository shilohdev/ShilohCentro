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
        query = "SELECT COUNT(a.id), a.id_responsavel, us.nome, DATE_FORMAT(a.data_registro,'%d/%m/%Y') FROM admins.ranking_atendimento a INNER JOIN auth_users.users us ON a.id_responsavel = us.id WHERE DATE_FORMAT(a.data_registro,'%d/%m/%Y') = DATE_FORMAT(CURRENT_DATE(),'%d/%m/%Y') group by a.id_responsavel, DATE_FORMAT(a.data_registro,'%d/%m/%Y'), us.nome ORDER BY COUNT(a.id) DESC LIMIT 5"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:
            for qtd, id, nome, data  in dados:
                nomes = nome.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2              
                newinfoa = ({ 
                    "data": data,
                    "id": id,
                    "nome": nome,
                    "qtd_day": qtd,
                    "nome": nome,
                    })                
                array.append(newinfoa)
        else:
            array.append({
                "qtd_day": '0',
            })
        return array


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
 

def _treating_data(ranking=None, photo=None):
    if ranking:
        for key in ranking:
            key["photo"] = photo.get(str(key.get('id'))).get('message')
    else:
        key = 0
    return key


 
#RANKING DASHBOARD ATENDIMENTO > MÊS
def RankingDashAtenMonthFunction(request):
    data_atual = str(datetime.now().strftime('%m/%Y'))
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT COUNT(a.id), a.id_responsavel, us.nome, DATE_FORMAT(a.data_registro,'%m/%Y') FROM admins.ranking_atendimento a INNER JOIN auth_users.users us ON a.id_responsavel = us.id WHERE DATE_FORMAT(a.data_registro,'%m/%Y') = DATE_FORMAT(CURRENT_DATE(), %s) group by a.id_responsavel, DATE_FORMAT(a.data_registro,'%m/%Y'), us.nome ORDER BY COUNT(a.id) DESC LIMIT 5"
        cursor.execute(query, (data_atual,))
        dados = cursor.fetchall()        
        array = []
        if dados:            
            for qtd, id, nome, data  in dados:
                nomes = nome.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2              
                newinfoa = ({ 
                    "data": data,
                    "id": id,
                    "nome": nome,
                    "qtd_month": qtd,
                    "nome": nome,
                    })                
                array.append(newinfoa)
        else:
            array.append({
                "qtd_month": '0',
            })
        return array


#RANKING DASHBOARD COMERCIAL > DIA
def RankingEnfermagemDayFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT b.nome, a.resp_enfermeiro, COUNT(a.status) AS qtd_concl FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users b ON b.id = a.resp_enfermeiro WHERE DATE(a.data_agendamento) = CURRENT_DATE() AND a.status = 'Concluído' group by b.id, b.nome, a.resp_enfermeiro ORDER BY qtd_concl DESC LIMIT 5;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:
            for nome, id_enfermeira, qtd in dados: 
                nomes = nome.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2              
                newinfoa = ({
                    "nome": nome,
                    "id_enfermeira": id_enfermeira,
                    "qtd_day": qtd                    
                    })                
                array.append(newinfoa)
            return array

#RANKING DASHBOARD ENFERMEIRAS > MÊS
def RankingEnfermagemMonthFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT b.nome, a.resp_enfermeiro, COUNT(a.status) AS qtd_mes FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users b ON b.id = a.resp_enfermeiro WHERE Month(a.data_agendamento) = Month(CURRENT_DATE()) AND a.status = 'Concluído' GROUP BY b.nome, a.resp_enfermeiro ORDER BY qtd_mes DESC LIMIT 5;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:            
            for nome, id, qtd_mes in dados:   
                nomes = nome.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2            
                newinfoa = ({
                    "nome": nome,
                    "id": id,
                    "qtd_month": qtd_mes                    
                    })                
                array.append(newinfoa)
            return array

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


def DashProdutividadeAgendamentoFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT COUNT(a.id), DATE_FORMAT(a.data_registro,'%d/%m/%Y') FROM admins.ranking_atendimento a INNER JOIN auth_users.users us ON a.id_responsavel = us.id WHERE acao = 'Agendou Coleta' AND DATE_FORMAT(a.data_registro,'%d/%m/%Y') = DATE_FORMAT(CURRENT_DATE(),'%d/%m/%Y') group by DATE_FORMAT(a.data_registro,'%d/%m/%Y')"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        if dados:
            for qtd, data in dados:
                newinfoa = ({
                    "qtd": qtd,
                    "data": data,                
                    })                
                array.append(newinfoa)
        else:
            array.append({
                "qtd": '0',
            })
        return array


def DashProdutividadePacienteFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT COUNT(a.id), DATE_FORMAT(a.data_registro,'%d/%m/%Y') FROM admins.ranking_atendimento a INNER JOIN auth_users.users us ON a.id_responsavel = us.id WHERE acao = 'Cadastrou Paciente' AND DATE_FORMAT(a.data_registro,'%d/%m/%Y') = DATE_FORMAT(CURRENT_DATE(),'%d/%m/%Y') group by DATE_FORMAT(a.data_registro,'%d/%m/%Y')"
        cursor.execute(query, )
        dados = cursor.fetchall()
        array = []
        if dados:
            for qtd, data in dados:
                newinfoa = ({
                    "qtd": qtd,
                    "data": data,                
                    })                
                array.append(newinfoa)
        else:
            array.append({
                "qtd": '0',
            })
        return array


def RankingCommerceDayFunction(request):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT b.id, b.nome, a.resp_comerce, COUNT(a.perfil) AS qtd_day FROM auth_users.users a INNER JOIN auth_users.users b ON b.id = a.resp_comerce WHERE DATE(a.data_regis) = CURRENT_DATE() AND a.perfil = '7' GROUP BY  b.id, b.nome, a.resp_comerce ORDER BY qtd_day DESC LIMIT 10;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:
            for id, nome, resp_comerce, qtd_day in dados: 
                nomes = nome.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2              
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "resp_comerce": resp_comerce,
                    "qtd_day": qtd_day                    
                    })                
                array.append(newinfoa)
        else:
            array.append({
                "qtd_day": '0',
            })
        return array


#RANKING DASHBOARD COMERCIAL > MÊS
def RankingCommerceMonthFunction(request):
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT b.id, b.nome, a.resp_comerce, COUNT(a.perfil) AS qtd_mes FROM auth_users.users a INNER JOIN auth_users.users b ON b.id = a.resp_comerce WHERE Month(a.data_regis) = Month(CURRENT_DATE()) AND a.perfil = '7' GROUP BY b.nome, a.resp_comerce ORDER BY qtd_mes DESC LIMIT 10;"
        cursor.execute(query )
        dados = cursor.fetchall()        
        array = []
        if dados:            
            for id, nome, resp_comerce, qtd_mes in dados:   
                nomes = nome.split()
                n1 = nomes[0]
                n2 = nomes[1]
                nome = n1 + " " + n2            
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "resp_comerce": resp_comerce,
                    "qtd_month": qtd_mes                    
                    })                
                array.append(newinfoa)
        else:
            array.append({
                "qtd_month": '0',
            })
        return array