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
from functions.general.decorator import convertDate, checkDayMonth
from django.forms import model_to_dict
from django.conf import settings
from django.core.files.storage import default_storage
import re

class FinancesExams:
    def __init__(self) -> None:
        self.cursor = Connection('userdb', '', '', '', '').connection()

    def schedule_collection(self, id):
        cursor = self.cursor
        params = (
            id,
        )
        query = "SELECT a.id, a.data_agendamento, a.hr_agendamento, b.tipo_servico, c.tipo_exame, g.nome_conv, e.nome, f.nome, np.nome_p, a.tel1_p, a.tel2_p, a.resp_medico, a.resp_atendimento, a. resp_comercial, a.cep, a.rua, a.numero, a.complemento, a.bairro, a.cidade, a.uf, a.val_cust, a.val_work_lab, a.val_pag, a.obs, b.tipo_servico, c.tipo_exame, a.status, a.motivo_status, co.color, np.login_conv, np.senha_conv FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN admins.health_insurance g ON a.convenio = g.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN auth_users.users f ON a.motorista = f.id INNER JOIN admins.status_colors co ON a.status = co.status_c INNER JOIN customer_refer.patients np ON a.nome_p = np.id_p WHERE a.id = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for a_id, a_data_agendamento, a_hr_agendamento, b_tipo_servico, c_tipo_exame, g_nome_conv, e_nome, f_nome, a_nome_p, a_tel1_p, a_tel2_p, a_resp_medico, a_resp_atendimento, a_resp_comercial, a_cep, a_rua, a_numero, a_complemento, a_bairro, a_cidade, a_uf, a_val_cust, a_val_work_lab, a_val_pag, a_obs, b_tipo_servico, c_tipo_exame, a_status, a_msotivo_tatus, co_color, login, senhaC  in dados:
                return {
                    "agendamento": {
                        "data_agendamento": a_data_agendamento,
                        "hr_agendamento": a_hr_agendamento,
                        "tipo_servico": b_tipo_servico,
                        "tipo_exame": c_tipo_exame,
                        "nurse": e_nome,
                        "motorista": f_nome,
                        "convenio": g_nome_conv,
                        "doctor": a_resp_medico,
                        "commerce": a_resp_comercial,
                        "id": a_id,

                    },
                    "pessoal": {
                        "phone1": a_tel1_p,
                        "phone2": a_tel2_p,
                        "paciente": a_nome_p,
                        "atendimento": a_resp_atendimento,
                    },
                    "endereco": {
                        "cep": a_cep,
                        "rua": a_rua,
                        "numero": a_numero,
                        "complemento": a_complemento,
                        "bairro": a_bairro,
                        "cidade": a_cidade,
                        "uf": a_uf,
                    },
                    "finance": {
                        "val_alv": a_val_cust,
                        "val_work": a_val_work_lab,
                        "val_pag": a_val_pag,
                        "date_frist": a_val_pag,
                    },
                    "obs": {
                        "obs": a_obs,
                        "statusM": a_status,
                        "motivo_status": a_msotivo_tatus,
                        "color": co_color,
                        "login": login,
                        "senhaC": senhaC,

                    }
                }

        return None

#SELECT DO FINANCEIRO AO INICIAR PROCESSO
    def fetch_exams(self, id):
        cursor = self.cursor

        params = (
            id,
        )
        query = "SELECT data_inc_proc_f, status_exame_f, resp_inicio_p_f, data_final_f FROM auth_finances.completed_exams WHERE id_agendamento_f = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        array = []
        if dados:
            for data_inc_proc_f, status_exame_f,  resp_inicio_p_f, data_final_f in dados:
                return {
                    "finances_exams": {
                        "status": str(status_exame_f) if status_exame_f else "",
                        "date_proccess": {
                            "start": data_inc_proc_f if data_inc_proc_f else "0000-00-00",
                            "end": data_final_f if data_final_f else "0000-00-00",
                        }
                    }
                }
        return array





class FinancesExamsInt:
    def __init__(self) -> None:
        self.cursor = Connection('userdb', '', '', '', '').connection()

    #MODAL  SELECT - PROCEDIMENTO INTERNO 
    def schedule_collectionInterno(self, id):
        cursor = self.cursor
        params = (
            id,
        )
        query = "SELECT a.id, a.data_agendamento, a.hr_agendamento, b.tipo_servico, c.tipo_exame, g.nome_conv, e.nome, np.nome_p, a.tel1_p, a.resp_atendimento, a.unity , a.perfil_int, a.val_cust, a.val_work_lab, a.val_pag, a.obs, a.status, a.motivo_status, co.color FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN admins.health_insurance g ON a.convenio = g.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN admins.status_colors co ON a.status = co.status_c INNER JOIN customer_refer.patients np ON a.nome_p = np.id_p WHERE a.identification LIKE 'Interno' AND a.id = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for a_id, a_data_agendamento, a_hr_agendamento, b_tipo_servico, c_tipo_exame, g_nome_conv, e_nome, np_nome_p, a_tel1_p, a_resp_atendimento, a_unity , a_perfil_int, a_val_cust, a_val_work_lab, a_val_pag, a_obs, a_status, a_motivo_status, co_color in dados:
                return{
                    "agendamento": {
                        "data_agendamento": a_data_agendamento,
                        "hr_agendamento": a_hr_agendamento,
                        "tipo_servico": b_tipo_servico,
                        "tipo_exame": c_tipo_exame,
                        "motorista": e_nome,
                        "nurse": e_nome,
                        "convenio": g_nome_conv,
                        "id": a_id,

                    },
                    "pessoal": {
                        "phone1": a_tel1_p,
                        "paciente": np_nome_p,
                        "atendimento": a_resp_atendimento,
                    },
                    "finance": {
                        "val_alv": a_val_cust,
                        "val_work": a_val_work_lab,
                        "val_pag": a_val_pag,
                        "date_frist": a_val_pag,
                    },
                    "obs": {
                        "obs": a_obs,
                        "statusM": a_status,
                        "motivo_status": a_motivo_status,
                        "color": co_color,
                        "unidade": a_unity,
                        "perfil": a_perfil_int,

                    }
                }
                   
        return None


#histórico financeiros
def fetchHistoryModalFinances(id):
    response = RegisterActions.objects.filter(id_agendamento=id)
    if list(response):
        r = [(model_to_dict(key)) for key in response]
        for j in r:
            j.update({
                "data_operacao": convertDate(j["data_operacao"])
            })
        return r
     
    return None


#MODAL SOLICITAÇÃO DE REEMBOLSO
def FunctionModalFinances(request):
    id = request.POST.get('id_user')

    files = fetchFileEditionsFinances(id)
    history = fetchHistoryModalFinances(id)
    filesInt = fetchFileEditionsFinancesInt(id)

    dict_response = {}
    with connections['auth_finances'].cursor() as cursor:
        params = (
            id,
        )
        query = "SELECT ef.id, ef.id_agendamento_f, ef.data_inc_proc_f, ef.status_exame_f, sf.status_p, ur.nome, ef.val_alvaro_f, ef.val_work_f, ef.val_pag_f, ef.porcentagem_paga_f, ef.data_repasse, ef.nf_f, ef.data_final_f, ef.data_registro_f, ef.resp_final_p_f FROM auth_finances.completed_exams ef INNER JOIN auth_users.users ur ON ef.resp_inicio_p_f = ur.id INNER JOIN auth_finances.status_progress sf ON ef.status_exame_f = sf.id WHERE ef.id_agendamento_f = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for ef_id, ef_id_agendamento_f, ef_data_inc_proc_f, ef_status_exame_f_id, ef_status_exame_f, ur_nome, ef_val_alvaro_f, ef_val_work_f, ef_val_pag_f, ef_porcentagem_paga_f, ef_data_repasse,  ef_nf_f, ef_data_final_f, ef_data_registro_f, ef_resp_final_p_f in dados:
                try:
                    ef_val_alvaro_f = f"R$ {ef_val_alvaro_f:_.2f}"
                    ef_val_alvaro_f = ef_val_alvaro_f.replace(".", ",").replace("_", ".")
                except:
                    pass

                try:
                    ef_val_work_f = f"R$ {ef_val_work_f:_.2f}" # f chama a função
                    ef_val_work_f = ef_val_work_f.replace(".", ",").replace("_", ".")
                    # f chama a função
                    # {} espaço para digitar a função
                    # f _.2f  >> informa que quer formatar o numero com _, em seguida informa quantas casa quer depois do _ e f de float
                except:
                    pass
                try:
                    ef_val_pag_f = f"R$ {ef_val_pag_f:_.2f}"
                    ef_val_pag_f = ef_val_pag_f.replace(".", ",").replace("_", ".")
                except:
                    pass
                
                try:
                    ef_porcentagem_paga_f = ef_porcentagem_paga_f / 100
                    ef_porcentagem_paga_f = f"{ef_porcentagem_paga_f:.0%}"
                    ef_porcentagem_paga_f = ef_porcentagem_paga_f.replace(".", ",").replace("_", ".")
                except:
                    pass
                dict_response = {
                    "dados": {
                        "id": ef_id, # id da linha
                        "pacient": ef_id_agendamento_f, # paciente
                        "date_start": convertDate(ef_data_inc_proc_f), #dia que começou o processo
                        "status_process": ef_status_exame_f,# status do processo
                        "status_process_id": ef_status_exame_f_id,# status do processo
                        "resp_start": ur_nome,#responsavel por iniciar
                        "val_alvaro": ef_val_alvaro_f,# valor alvaro
                        "val_work": ef_val_work_f,# valor worklab
                        "val_pago": ef_val_pag_f,# valor pago
                        "por_paga": ef_porcentagem_paga_f,# porcentagem paga
                        "date_repass": ef_data_repasse,# nota fiscal
                        "nf": ef_nf_f,# nota fiscal
                        "date_end": convertDate(ef_data_final_f) ,# data final do processo
                        "data_regis": ef_data_registro_f,# data registro
                        "resp_end": ef_resp_final_p_f,# responsavel por finalizar
                    },
                    "files": json.dumps(files),
                    "filesInt": json.dumps(filesInt),
                    "history": history
                } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
        else:
            dados = Exams.objects.filter(id_agendamento_f=id).first()
            if dados:
                dict_response = {
                    "dados": {
                        "id": dados.id, # id da linha
                        "pacient": dados.id_agendamento_f, # paciente
                        "date_start": convertDate(dados.data_inc_proc_f), #dia que começou o processo
                        "status_process": dados.status_exame_f,# status do processo
                        "resp_start": dados.resp_inicio_p_f,#responsavel por iniciar
                        "val_alvaro": dados.val_alvaro_f,# valor alvaro
                        "val_work": dados.val_work_f,# valor worklab
                        "val_pago": dados.val_pag_f,# valor pago
                        "por_paga": dados.porcentagem_paga_f,# porcentagem paga
                        "date_repass": dados.data_repasse,# data do reembolso
                        "nf": dados.nf_f,# nota fiscal
                        "date_end": dados.data_final_f,# data final do processo
                        "data_regis": dados.data_registro_f,# data registro
                        "resp_end": dados.resp_final_p_f,# responsavel por finalizar
                    },
                    "files": json.dumps(files),
                    "filesInt": json.dumps(filesInt),
                    "history": history
                }


    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT
    }

 
#GET FILE >> ADICIONAR DIRETORIO
def saveFileEditionsFinances(id, etype, FILES): #CRIA O DIRETÓRIO DOS DOCUMENTOS
    with connections['auth_users'].cursor() as cursor:
        params = (
            id,
        )
        query = "SELECT id, nome_p, identification FROM auth_agenda.collection_schedule WHERE id LIKE %s;"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for id, nome, identificacao in dados:
                if identificacao == "Externo":
                    PATH = settings.BASE_DIR_DOCS + "/patients/process/{}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
                    PATH_USER = PATH.format(id) # ADICIONANDO ID NO {} DE CIMA /\
                    PATH_TYPES = PATH_USER + "/" + etype + "/" # AQUI ESTÁ INDO PARA O DIRETORIO: docs/patients/process/ID/tipo_do_arquivo
                    arr_dir = []
                    for name, file in FILES.items():
                        file_name = default_storage.save(PATH_TYPES + file.name, file)
                        arr_dir.append({
                            "name": file.name,
                            "path": PATH_TYPES + file.name
                        })
                else: 
                    PATH = settings.BASE_DIR_DOCS + "/user/process/{}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
                    PATH_USER = PATH.format(id) # ADICIONANDO ID NO {} DE CIMA /\
                    PATH_TYPES = PATH_USER + "/" + etype + "/" 
                    arr_dir = []

                    for name, file in FILES.items():
                        file_name = default_storage.save(PATH_TYPES + file.name, file)
                        arr_dir.append({
                            "name": file.name,
                            "path": PATH_TYPES + file.name
                        })

        return True


#GER FILE
def fetchFileEditionsFinances(id):

    arr_files = []

    ORIGIN_PATH = f"/patients/process/{id}"
    PATH = settings.BASE_DIR_DOCS + f"/patients/process/{id}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    EXISTS = default_storage.exists(PATH)
    if EXISTS:
        FILES = default_storage.listdir(PATH)
        FILES = list(FILES)[0]
        for keys in FILES:
            n = (str(((str(keys).replace("[", "")).replace("]", "")).replace("'", "")).replace(" ", "")).split(",")
            for key in n:
                key = ((str(key).replace("[", "")).replace("]", "")).replace("'", "")
                PATH_TYPE = PATH + f"/{key}"
                ORIGIN_PATH_TYPE = ORIGIN_PATH + f"/{key}"
                for fkey in default_storage.listdir(PATH_TYPE):
                    if type(fkey) != list:
                        if fkey not in ["", None]:
                            fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                            if len(fkey) > 1:
                                PATH_FILE = PATH_TYPE + f"/{fkey}"
                                ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                arr_files.append({
                                    "type": key,
                                    "description_type": settings.LISTPATHTYPE.get(key, ""),
                                    "file": {
                                        "name": fkey,
                                        "date_created": {
                                            "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                            "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                        },
                                        "path": ORIGIN_PATH_FILE
                                    }
                                })
                    else:
                        for fkey in fkey:
                            if fkey not in ["", None]:
                                fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                                if len(fkey) > 1:
                                    PATH_FILE = PATH_TYPE + f"/{fkey}"
                                    ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                    arr_files.append({
                                        "type": key,
                                        "description_type": settings.LISTPATHTYPE.get(key, ""),
                                        "file": {
                                            "name": fkey,
                                            "date_created": {
                                                "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                                "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                            },
                                            "path": ORIGIN_PATH_FILE
                                        }
                                    })
    return arr_files
 


#GER FILE 
def fetchFileEditionsFinancesInt(id):

    arr_files = []

    ORIGIN_PATH = f"/user/process/{id}"
    PATH = settings.BASE_DIR_DOCS + f"/user/process/{id}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    EXISTS = default_storage.exists(PATH)
    if EXISTS:
        FILES = default_storage.listdir(PATH)
        FILES = list(FILES)[0]
        for keys in FILES:
            n = (str(((str(keys).replace("[", "")).replace("]", "")).replace("'", "")).replace(" ", "")).split(",")
            for key in n:
                key = ((str(key).replace("[", "")).replace("]", "")).replace("'", "")
                PATH_TYPE = PATH + f"/{key}"
                ORIGIN_PATH_TYPE = ORIGIN_PATH + f"/{key}"
                for fkey in default_storage.listdir(PATH_TYPE):
                    if type(fkey) != list:
                        if fkey not in ["", None]:
                            fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                            if len(fkey) > 1:
                                PATH_FILE = PATH_TYPE + f"/{fkey}"
                                ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                arr_files.append({
                                    "type": key,
                                    "description_type": settings.LISTPATHTYPE.get(key, ""),
                                    "file": {
                                        "name": fkey,
                                        "date_created": {
                                            "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                            "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                        },
                                        "path": ORIGIN_PATH_FILE
                                    }
                                })
                    else:
                        for fkey in fkey:
                            if fkey not in ["", None]:
                                fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                                if len(fkey) > 1:
                                    PATH_FILE = PATH_TYPE + f"/{fkey}"
                                    ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                    arr_files.append({
                                        "type": key,
                                        "description_type": settings.LISTPATHTYPE.get(key, ""),
                                        "file": {
                                            "name": fkey,
                                            "date_created": {
                                                "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                                "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                            },
                                            "path": ORIGIN_PATH_FILE
                                        }
                                    })


    return arr_files
 


#SALVAR MODAL FINANCEIRO  - AGENDAMENTO CONCLUIDO PROCESSO INICIADO
def SaveEditionsFinancesFunctions(request):
    id_user = request.POST.get('id_user')
    type_doc = request.POST.get('type_doc')
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cust_alv = request.POST.get('cust_alv')
    val_w_lab = request.POST.get('val_w_lab')
    val_pago = request.POST.get('val_pago')
    porcentagem = request.POST.get('porcentagem')

    saveFileEditionsFinances(id_user, type_doc, request.FILES)
    bodyData = json.loads(request.POST.get('data'))
    
    nomeStatus = bodyData.get('statusProgresso')
    obsF = bodyData.get('obsF')

    dataKeys = { #DICT PARA PEGAR TODOS OS VALORES DO AJAX
        "tp_perfil": "perfil", #key, value >> valor que vem do ajax, valor para onde vai (banco de dados)
        "date_repass": "data_repasse",
        "n_nf": "nf_f",
        "statusProgresso": "status_exame_f",
        "obsF": "obs_f",
    }
    with connections['auth_finances'].cursor() as cursor:
            searchID = "SELECT id, nome FROM auth_users.users WHERE login LIKE %s"
            cursor.execute(searchID, (request.user.username,))
            dados = cursor.fetchall()
            if dados:
                for id_usuario, nome in dados:
                    pass
            else:
                return {
                    "response": "false",
                    "message": "Login expirado, faça login novamente para continuar."
                }
            for key in dataKeys:
                if key in bodyData:#SE MEU VALOR DO INPUT DO AJAX EXISTIR DENTRO DO MEU POST, FAZ A QUERY
                    vData = bodyData.get(key)
                    if key == "date_repass":
                        vData = vData if vData not in ["", None] else None

                    alvaro = float (cust_alv) if cust_alv not in ["", None] else None #serve para aceitar campo null quando double
                    worklab = float (val_w_lab) if val_w_lab not in ["", None] else None #serve para aceitar campo null quando double
                    pago = float (val_pago) if val_pago not in ["", None] else None #serve para aceitar campo null quando double
                    porcentagem = float (porcentagem) if porcentagem not in ["", None] else None #serve para aceitar campo null quando double

                    query = "UPDATE auth_finances.completed_exams SET {} = %s, val_alvaro_f = %s,  val_work_f = %s, val_pag_f = %s, porcentagem_paga_f = %s WHERE id_agendamento_f = %s".format(dataKeys[key]) #format serve para aplicar o método de formatação onde possui o valor da minha var dict e colocar dentro da minha chave, para ficar no padrão de UPDATE banco
                    params = (
                        vData,
                        alvaro,
                        worklab,
                        pago,
                        porcentagem, #serve para complementar o POST e obter o valor do input
                        id_user,
                    )
                    cursor.execute(query, params)

            if obsF == '':
                query9 = "SELECT id, status_p FROM auth_finances.status_progress where id like %s"
                param =(nomeStatus,)
                cursor.execute(query9, param)
                dados = cursor.fetchall()
                array = []
                        
                for idP, nomeStatus in dados:
                    newinfoa = ({
                        "id": idP,
                        "nomeStatus": nomeStatus,
                        })
                    array.append(newinfoa)
                query2 = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `id_agendamento`, `tp_operacao`, `nome_user`, `descricao`, `data_operacao`) VALUES (NULL, '1', %s, 'Salvar Modal',  %s, 'Salvou o cadastro | Status do Processo: ' %s , %s);"
                params2 = (
                    id_user, nome, nomeStatus, date_create, 
                )
                cursor.execute(query2, params2)
            else:
                query2 = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `id_agendamento`, `tp_operacao`, `nome_user`, `descricao`, `data_operacao`) VALUES (NULL, '1', %s, 'Salvar Modal',  %s, 'Salvou o cadastro | Status do Processo: ' %s , %s);"
                params2 = (
                    id_user, nome, nomeStatus, date_create, 
                )
                cursor.execute(query2, params2)

                query4 = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `id_agendamento`, `tp_operacao`, `nome_user`, `descricao`, `data_operacao`) VALUES (NULL, '1', %s, 'Salvar Modal',  %s, 'Observação: ' %s, %s);"

                params4 = (
                    id_user, nome, obsF, date_create,
                )
                cursor.execute( query4, params4)
            
            if type_doc != '':
                queryS = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `id_agendamento`, `tp_operacao`, `nome_user`, `descricao`, `data_operacao`) VALUES (NULL, '1', %s, 'Salvar Modal',  %s, 'Inseriu um Anexo', %s);"
                paramS =( id_user, nome, date_create,)
                cursor.execute(queryS,paramS )

            if nomeStatus == 'Glosa': #aqui
                queryG = "UPDATE `auth_finances`.`completed_exams` SET `def_glosado_n_atingido` = '1' WHERE `id_agendamento_f` = %s"
                paramG =( id_user,)
                cursor.execute(queryG,paramG )
               
               
            
            if nomeStatus == 'Valor Não Atingido': #aqui
                queryN = "UPDATE `auth_finances`.`completed_exams` SET `def_glosado_n_atingido` = '2' WHERE `id_agendamento_f` = %s"
                paramN =( id_user,)
                cursor.execute(queryN,paramN )
              
              

            return {
                "response": True,
                "message": "Dados atualizados com sucesso."
            }



#FINALIZAR  PROCESSO REEMBOLSO
def FinalizeProcessFunction(request):
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    id_agendamento = request.POST.get("id_user")
    statusProgresso = request.POST.get("statusProgresso")
    ValorPago = request.POST.get("ValorPago").replace("R$","").replace(".","").replace(",",".")
    doctor = request.POST.get("doctor")
    paciente = request.POST.get("paciente")
    comercial = request.POST.get("comercial")
    repasse = request.POST.get("date_repass")
    date_age = request.POST.get("date_age")
    tp_exame = request.POST.get("tp_exame")
    
    with connections['admins'].cursor() as cursor:        
        searchID = "SELECT id, nome FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        #atualização de status
        param = ( repasse, statusProgresso, date_create, id_usuario, id_agendamento,)
        query = "UPDATE `auth_finances`.`completed_exams` SET `data_repasse` = %s,  `status_exame_f` = %s, `data_final_f` = %s,  `resp_final_p_f` = %s, `regis` = '1' WHERE (`id_agendamento_f` = %s);"
        cursor.execute(query, param)
        #historico de atualização 
        query2 = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `id_agendamento`, `tp_operacao`, `nome_user`, `descricao`, `data_operacao`) VALUES (NULL, '1', %s, 'Finalizar Processo',  %s, 'Finalizou o processo de reembolso', %s);"
        params2 = (
            id_agendamento, nome, date_create, 
        )
        cursor.execute(query2, params2)


        queryVerif = "SELECT id, id_agendamento FROM auth_finances.closing_finance WHERE id_agendamento LIKE %s "
        cursor.execute(queryVerif, (id_agendamento,))
        dados = cursor.fetchall()
        if dados: 
            for id, id_agendamento in dados:
                return {
                "response": "true",
                "message": "Processo de reembolso já finalizado."
            }
        else:
            pass

        if statusProgresso == '4':
            queryVal = "SELECT perfil, id, nome, val_padrao, val_porcentagem, val_fixo FROM auth_users.users WHERE nome LIKE %s"            
            paramsVal = (
                doctor,
            )
            cursor.execute(queryVal, paramsVal)
            dadosMEDICO = cursor.fetchall()

            for perfil, id, nome, val_padrao, val_porcentagem, val_fixo in dadosMEDICO:
                SelectIndicacao="SELECT b.nome_p, a.data_regis_l, a.medico_resp_l as medico, c.resp_comerce as comercial FROM customer_refer.leads a INNER JOIN customer_refer.patients b ON b.id_l_p = a.id_lead INNER JOIN auth_users.users c ON a.medico_resp_l = c.id WHERE a.medico_resp_l = %s"
                cursor.execute(SelectIndicacao, (id,))
                dados = cursor.fetchall()
                array2 = []

                val_padrao =  (val_padrao) if val_padrao not in ["", None] else None
                val_porcentagem = (val_porcentagem) if val_porcentagem not in ["", None] else None
                val_fixo =  (val_fixo) if val_fixo not in ["", None] else None

                for pacienteS, data_indicacaoS, medicoS, comercialS in dados:
                    newinfoa = ({
                        "paciente": pacienteS,
                        "data_indicacao": data_indicacaoS,
                        "medico": medicoS,
                        "comercial": comercialS,
                        })
                    array2.append(newinfoa)
                
                    if perfil == '7':
                        if val_porcentagem:
                        
                            val_porcentagem = float(val_porcentagem)
                            ValorPago = float(ValorPago)
                            porcentagem = float(val_porcentagem / 100) * float(ValorPago)
                            porcentagem = f'{porcentagem:.2f}'

                            queryFinance ="INSERT INTO `auth_finances`.`closing_finance` (`id`,  `id_agendamento`, `nome_medico`, `nome_paciente`, `nome_comercial`, `data_coleta`, `data_repasse`, `data_indicação`, `exame`, `valor_uni_partners`, `valor_comercial`, `status_partners`, `status_comercial`, `data_pag_partners`, `data_pag_comercial`, `resp_pag_partners`, `resp_pag_comercial`, `data_regis`) VALUES (NULL, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pendente', 'Pendente', '1969-12-31 00:00:00', '1969-12-31 00:00:00', '', '', %s);"
                            val_comercial = float(porcentagem) * float(0.10)
                            paramsFinance = (id_agendamento, id, paciente, comercialS, date_age, repasse, data_indicacaoS, tp_exame, porcentagem, val_comercial, date_create,)
                            cursor.execute(queryFinance, paramsFinance)
                    
                        elif val_padrao:
                            val_padrao = float(val_padrao)
                            queryFinance ="INSERT INTO `auth_finances`.`closing_finance` (`id`, `id_agendamento`, `nome_medico`, `nome_paciente`, `nome_comercial`, `data_coleta`, `data_repasse`, `data_indicação`, `exame`, `valor_uni_partners`, `valor_comercial`, `status_partners`, `status_comercial`, `data_pag_partners`, `data_pag_comercial`, `resp_pag_partners`, `resp_pag_comercial`, `data_regis`) VALUES (NULL, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pendente', 'Pendente', '1969-12-31 00:00:00', '1969-12-31 00:00:00', '', '', %s);"
                            val_comercial = float(val_padrao) * float(0.10)
                            paramsFinance = (id_agendamento, id, paciente, comercialS, date_age, repasse, data_indicacaoS, tp_exame, val_padrao, val_comercial, date_create,)
                            cursor.execute(queryFinance, paramsFinance)
                        
                        else:
                            val_fixo = float(val_fixo)
                            queryFinance ="INSERT INTO `auth_finances`.`closing_finance` (`id`, `id_agendamento`, `nome_medico`, `nome_paciente`, `nome_comercial`, `data_coleta`, `data_repasse`, `data_indicação`, `exame`, `valor_uni_partners`, `valor_comercial`, `status_partners`, `status_comercial`, `data_pag_partners`, `data_pag_comercial`, `resp_pag_partners`, `resp_pag_comercial`, `data_regis`) VALUES (NULL, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pendente', 'Pendente', '1969-12-31 00:00:00', '1969-12-31 00:00:00', '', '', %s);"
                            val_comercial = float(val_fixo) * float(0.10)
                            paramsFinance = (id_agendamento, id, paciente, comercialS, date_age, repasse, data_indicacaoS, tp_exame, val_fixo, val_comercial, date_create,)
                            cursor.execute(queryFinance, paramsFinance)
                    else:
                        queryFinance ="INSERT INTO `auth_finances`.`closing_finance` (`id`, `id_agendamento`, `nome_medico`, `nome_paciente`, `nome_comercial`, `data_coleta`, `data_repasse`, `data_indicação`, `exame`, `valor_uni_partners`, `valor_comercial`, `status_partners`, `status_comercial`, `data_pag_partners`, `data_pag_comercial`, `resp_pag_partners`, `resp_pag_comercial`, `data_regis`) VALUES (NULL, %s,%s, %s, %s, %s, %s, %s, %s, %s, '0', 'Pendente', 'Pendente', '1969-12-31 00:00:00', '1969-12-31 00:00:00', '', '', %s);"
                        paramsFinance = (id_agendamento, id, paciente, comercialS, date_age, repasse, data_indicacaoS, tp_exame, val_padrao, date_create,)
                        cursor.execute(queryFinance, paramsFinance)
        else:
            return {"message":"Não foi possível encontrar este paciente."}

    return {"response": "true", "message": "Processo Financeiro Finalizado!"}


#REEMBOLSO FINALIZADO - TABELA COM TODOS CONCLUIDOS aquyy
def searchrRefundCompletedFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id INNER JOIN  admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE  a.status = 'Concluído' AND sp.regis LIKE  '1';"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
        
        for id, paciente, coleta, inicioP, fimP, exame, status_p, unidade in dados:
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "coleta": convertDate(coleta),
                "inicioP": convertDate(inicioP),
                "fimP": convertDate(fimP),
                "exame": exame,
                "status_p": status_p,
                "unidade": unidade,
                })
            array.append(newinfoa)
    return array


#SELECT POR MES
def SearchMonthExamsConclFunction(request):
    month = request.POST.get('month')
    data1 = request.POST.get('data1')
    data2 = request.POST.get('data2')
    statusProgresso = request.POST.get('statusProgressoF')
    
    with connections['auth_agenda'].cursor() as cursor:
        params =(data1, data2, statusProgresso,)
        if data1 and data2 and statusProgresso != "":
            data1 = data1 + ' 00:00:00'
            data2 = data2 + ' 23:59:59'
            query = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id INNER JOIN admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE sp.data_final_f BETWEEN %s AND %s AND a.status = 'Concluído' AND sp.regis LIKE  '1' AND spa.status_p = %s"
            cursor.execute(query, params)
            dados = cursor.fetchall()
            array = []
            for id, paciente, coleta, inicioP, fimP, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "inicioP": convertDate(inicioP),
                    "fimP": convertDate(fimP),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)
        elif statusProgresso != "":
            query = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id INNER JOIN  admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE a.status = 'Concluído' AND sp.regis LIKE  '1' AND spa.status_p = %s"
            cursor.execute(query, (statusProgresso,))
            dados = cursor.fetchall()
            array = []
            for id, paciente, coleta, inicioP, fimP, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "inicioP": convertDate(inicioP),
                    "fimP": convertDate(fimP),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)
        elif data1 and data2 != "":
            queryd = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, ex.tipo_exame, spa.status_p, uni.unit_s  FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id INNER JOIN  admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE sp.data_final_f BETWEEN %s AND %s AND a.status = 'Concluído' AND sp.regis LIKE  '1';"
            data1 = data1 + ' 00:00:00'
            data2 = data2 + ' 23:59:59'
            cursor.execute(queryd, (data1,data2,))
            dados = cursor.fetchall()
            array = []
            for id, paciente, coleta, inicioP, fimP, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "inicioP": convertDate(inicioP),
                    "fimP": convertDate(fimP),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)

        else:
            queryd = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, ex.tipo_exame, spa.status_p, uni.unit_s  FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id INNER JOIN  admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE a.status = 'Concluído' AND sp.regis LIKE  '1';"
            cursor.execute(queryd)
            dados = cursor.fetchall()
            array = []
            for id, paciente, coleta, inicioP, fimP, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "inicioP": convertDate(inicioP),
                    "fimP": convertDate(fimP),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)


    return {
        "response": "true",
        "message": array
    }



#SELECT TABELA HISTORICO
def historicExamConclFunction(id):
    with connections['admins'].cursor() as cursor:
        param=(id,)
        query = "SELECT nome_user, descricao, data_operacao FROM admins.register_actions WHERE id_agendamento = %s"
        cursor.execute(query, param)
        dados = cursor.fetchall()
        array = []
        for name, descrition, date in dados:
            newiRegis = ({
                "name": name,
                "descrition": descrition,
                "date": convertDate(date)
                })
            array.append(newiRegis)

        return array
             
      
#SELECT STATUS PROCESSO NEGATIVO
def FunctionStatusN(request):
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT id, status_progress_n FROM auth_finances.status_progress_negative"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
        for id, status in dados:
            newinfoa = ({
                "idn": id,
                "statusn": status,
                })
            array.append(newinfoa)
    return array



#TABELA STATUS NEGATIVO > VALOR NÃO ATINGIDO  aquyt
def searchNotReached(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' AND spa.status_p NOT LIKE 'Cancelado' AND sp.identification LIKE 'Externo' AND sp.def_glosado_n_atingido LIKE '2';"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
            
        for id, paciente, comercial, medico, dataconc, status, status_p in dados:
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "comercial": comercial,
                "medico": medico,
                "dataconc": convertDate(dataconc),
                "status": status,
                "status_p": status_p,
                })
            array.append(newinfoa)
    return array



#TABELA STATUS NEGATIVO > GLOSA
def searchGlosses(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' AND sp.identification LIKE 'Externo' AND spa.status_p NOT LIKE 'Cancelado' AND sp.def_glosado_n_atingido LIKE '1';"
        cursor.execute(query,)
        dados = cursor.fetchall()
        array = []
            
        for id, paciente, comercial, medico, dataconc, status, status_p in dados:
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "comercial": comercial,
                "medico": medico,
                "dataconc": convertDate(dataconc),
                "status": status,
                "status_p": status_p,
                })
            array.append(newinfoa)
    return array


#-----------------------------------------------------------------------------------------------------
#FINANCEIRO > INTERNO 
#TABELA SELECT SOLICITAÇÕES
def searchSolicitationsInt(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.data_fin, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' and spa.status_p NOT LIKE 'Glosado' and spa.status_p NOT LIKE 'Valor Não Atingido' AND a.identification LIKE 'Interno';"
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
            
        for id, paciente, dataconc, status, status_p in dados:
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "dataconc": convertDate(dataconc),
                "status": status,
                "status_p": status_p,
                })
            array.append(newinfoa)
    return array

#-----------------------------------------------------------



#SELECT POR MES
def pesqMesInternoFinalizados(request):
    month = request.POST.get('month')
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE  a.status = 'Concluído' AND sp.regis LIKE  '1' AND a.identification LIKE  'Interno' AND DATE_FORMAT(sp.data_final_f, '%m') = %s"
        cursor.execute(query, (month,))
        dados = cursor.fetchall()
        array = []

        for id, paciente, coleta, inicioP, fimP, status, status_p in dados:
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "coleta": convertDate(coleta),
                "inicioP": convertDate(inicioP),
                "fimP": convertDate(fimP),
                "status": status,
                "status_p": status_p,
                })
            array.append(newinfoa)

    return {
        "response": "true",
        "message": array
    }


#SELECT POR MES
def SearchMonthSolicitation(request):
    month = request.POST.get('month')
    data1 = request.POST.get('data1')
    data2 = request.POST.get('data2')
    statusProgressoF = request.POST.get('statusProgressoF')
    with connections['auth_agenda'].cursor() as cursor:
        params= (data1, data2, statusProgressoF,)
        if data1 and data2 and statusProgressoF != "":
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.data_agendamento BETWEEN %s AND %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE 'Interno' AND spa.status_p = %s; "
            cursor.execute(query, params)
            dados = cursor.fetchall()
            array = []

            for id, paciente, dataconc, status, status_p in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "dataconc": convertDate(dataconc),
                    "status": status,
                    "status_p": status_p,
                    })
                array.append(newinfoa)

        elif data1 and data2 != "":
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.data_agendamento BETWEEN %s AND %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE 'Interno'; "
            cursor.execute(query, (data1, data2))
            dados = cursor.fetchall()
            array = []

            for id, paciente, dataconc, status, status_p in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "dataconc": convertDate(dataconc),
                    "status": status,
                    "status_p": status_p,
                    })
                array.append(newinfoa)

        if statusProgressoF != "":
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE 'Interno' AND spa.status_p = %s; "
            cursor.execute(query, (statusProgressoF,))
            dados = cursor.fetchall()
            array = []

            for id, paciente, dataconc, status, status_p in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "dataconc": convertDate(dataconc),
                    "status": status,
                    "status_p": status_p,
                    })
                array.append(newinfoa)

        else:
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE 'Interno'; "
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []

            for id, paciente, dataconc, status, status_p in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "dataconc": convertDate(dataconc),
                    "status": status,
                    "status_p": status_p,
                    })
                array.append(newinfoa)

    return {
        "response": "true",
        "message": array
    }


#SELECT POR MES SOLICITAÇÃO DE REEMBOLSO EXTERNA aquiy
def SearchMonthExamsRefundF(request):
    month = request.POST.get('month')
    data1 = request.POST.get('data1')
    data2 = request.POST.get('data2')
    statusProgressoTable = request.POST.get('statusProgressoTable')
    with connections['auth_agenda'].cursor() as cursor:
        
        searchID = "SELECT a.perfil, a.id, a.nome, a.unity FROM auth_users.users a INNER JOIN admins.units_shiloh b ON a.unity = b.id_unit_s WHERE login LIKE %s "
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for perfil, id_usuario, nome, unityY in dados: 
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        
        params = (unityY, data1, data2, statusProgressoTable,)
        if data1 and data2 and statusProgressoTable != "" : 
            query = "SELECT a.id, pa.nome_p, a.data_agendamento,  ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN admins.units_shiloh uni ON pa.unity_p = uni.id_unit_s INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id WHERE uni.id_unit_s like %s AND  data_agendamento BETWEEN %s AND %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE  'Externo' AND status_p = %s;"
            cursor.execute(query, params)
            dados = cursor.fetchall()
            array = []

            for id, paciente, coleta, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)
        elif statusProgressoTable != "":
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN admins.units_shiloh uni ON pa.unity_p = uni.id_unit_s INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id WHERE uni.id_unit_s like %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE  'Externo' AND status_p = %s;"
            cursor.execute(query, (unityY, statusProgressoTable,))
            dados = cursor.fetchall()
            array = []

            for id, paciente, coleta, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)
        elif  data1 and data2 != "":
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN admins.units_shiloh uni ON pa.unity_p = uni.id_unit_s INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id WHERE uni.id_unit_s like %s AND data_agendamento BETWEEN %s AND %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE  'Externo';"
            cursor.execute(query, (unityY, data1, data2,))
            dados = cursor.fetchall()
            array = []

            for id, paciente, coleta, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)
        else:
            query = "SELECT a.id, pa.nome_p, a.data_agendamento, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN admins.units_shiloh uni ON pa.unity_p = uni.id_unit_s INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id WHERE uni.id_unit_s like %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE  'Externo';"
            cursor.execute(query, (unityY,))
            dados = cursor.fetchall()
            array = []

            for id, paciente, coleta, exame, status_p, unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "coleta": convertDate(coleta),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    })
                array.append(newinfoa)
                
        


    return {
        "response": "true",
        "message": array
    }

#---------------------------------------------------- FECHAMENTO PARCEIROS ---------------------------------------------------------


#TABELA FECHAMENTO PARCEIROS estou aqui1
def TableClosingPartners(request):
    month = int(datetime.now().strftime("%m"))

    with connections['auth_finances'].cursor() as cursor:
        #query = "SELECT b.id, b.nome, c.categoria, co.nome, b.rn, month( a.data_repasse) AS mes_repasse, SUM(a.valor_uni_partners) AS total, a.status_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id INNER JOIN auth_users.users co ON a.nome_comercial = co.id INNER JOIN auth_users.Category_pertners c ON b.categoria = c.id WHERE valor_comercial != 0 AND MONTH( a.data_repasse) LIKE %s GROUP BY a.nome_medico, co.nome, b.rn, MONTH( a.data_repasse), b.id, a.status_partners"
        query = "SELECT b.id, b.nome, c.categoria, co.nome, b.rn, month( a.data_repasse) AS mes_repasse, SUM(a.valor_uni_partners) AS total, a.status_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id INNER JOIN auth_users.users co ON a.nome_comercial = co.id INNER JOIN auth_users.Category_pertners c ON b.categoria = c.id WHERE valor_uni_partners != 0 AND MONTH( a.data_repasse) LIKE %s GROUP BY a.nome_medico, co.nome, b.rn, MONTH( a.data_repasse), b.id, a.status_partners"
        cursor.execute(query, (month,))
        dados = cursor.fetchall()
        array = []
        for id, medico, categoria, comercial, rn, data_repasse, valor, status in dados:
            if dados == empty:
                array.append("nenhumm dado")
            else:
                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "id": id,
                    "medico": medico,
                    "rn": rn,
                    "categoria": categoria,
                    "comercial": comercial,
                    "data_repasse": data_repasse,
                    "valor": valor,
                    "status": status,
                    })
                array.append(newinfoa)
        return array

#VALOR TOTAL FECHAMENTO DOS PARCEIROS
def valTotalPartinersF(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:

        querys = "SELECT COUNT(DISTINCT nome_medico) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s  AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
        cursor.execute(querys, (monthCount,))
        dados = cursor.fetchall()
        array2 = []
        if dados:
            for qdt, val, mes in dados:
                val = f"R$ {val:_.2f}"
                val = val.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": val,
                    "mes": mes,
                    })
                array2.append(newinfoa)
        return array2



#VALOR TOTAL FECHAMENTO DOS PARCEIROS - A PAGAR
def valPartinersPending(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:

        querys = "SELECT COUNT(DISTINCT nome_medico) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE status_partners LIKE 'Pendente' AND MONTH(data_repasse) LIKE %s  AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
        cursor.execute(querys, (monthCount,))
        dados = cursor.fetchall()
        array2 = []
        if dados:
            for qdt, val, mes in dados:
                val = f"R$ - {val:_.2f}"
                val = val.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": val,
                    "mes": mes,
                    })
                array2.append(newinfoa)
        return array2


#VALOR TOTAL FECHAMENTO DOS PARCEIROS - PAGO
def valPartinersPay(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:

        querys = "SELECT COUNT(DISTINCT nome_medico) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE status_partners LIKE 'Pago' AND MONTH(data_repasse) LIKE %s  AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
        cursor.execute(querys, (monthCount,))
        dados = cursor.fetchall()
        array2 = []
        if dados:
            for qdt, val, mes in dados:
                val = f"R$ {val:_.2f}"
                val = val.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": val,
                    "mes": mes,
                    })
                array2.append(newinfoa)
        return array2


#FILTRO TABELA FECHAMENTO PARCEIROS >>> estoy naqui 
def FilterMonthClosingPartners(request):
    month = request.POST.get('month')
    monthCount = (datetime.now().strftime("%m"))
    
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT b.id, b.nome, c.categoria, co.nome, b.rn, month( a.data_repasse) AS mes_repasse, SUM(a.valor_uni_partners) AS total, a.status_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id INNER JOIN auth_users.users co ON a.nome_comercial = co.id INNER JOIN auth_users.Category_pertners c ON b.categoria = c.id WHERE MONTH( a.data_repasse) LIKE %s GROUP BY a.nome_medico, co.nome, b.rn, MONTH( a.data_repasse), b.id, a.status_partners"
        cursor.execute(query, (month,))
        dados = cursor.fetchall()
        array = []
        if dados:
            for id, medico, categoria, comercial, rn, data_repasse, valor, status in dados:
                valor = (valor) if valor not in ["", None] else None
                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "id": id,
                    "medico": medico,
                    "rn": rn,
                    "categoria": categoria,
                    "comercial": comercial,
                    "data_repasse": data_repasse,
                    "valor": valor,
                    "status": status,
                    })
                array.append(newinfoa)
            
        querys = "SELECT COUNT(DISTINCT nome_medico) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
        cursor.execute(querys, (month,))
        dados = cursor.fetchall()
        array2 = []
        if dados:
            for qdt, val, mes in dados:
                val = f"R$ {val:_.2f}"
                val = val.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": val,
                    "mes": mes,
                    })
                array2.append(newinfoa)
        
        querysP = "SELECT COUNT(DISTINCT nome_medico) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE status_partners LIKE 'Pago' AND MONTH(data_repasse) LIKE %s AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
        cursor.execute(querysP, (month,))
        dados = cursor.fetchall()
        array3 = []
        if dados:
            for qdts, vals, mes in dados:
                vals = f"R$ {vals:_.2f}"
                vals = vals.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdts,
                    "val": vals,
                    "mes": mes,
                    })
                array3.append(newinfoa)

        querysA = "SELECT COUNT(DISTINCT nome_medico), SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE  MONTH(data_repasse) LIKE %s AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
        cursor.execute(querysA, (month,))
        dados = cursor.fetchall()
        array4 = []
        if dados:
            for qdt, val, mes in dados:
                qdt =  qdt - qdts
                vals = vals.replace("R$","").replace(".","").replace(",",".").replace(" ","")   
                vals = float(vals) - float(val)
                vals = f"R$ {vals:_.2f}"
                vals = vals.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": vals,
                    "mes": mes,
                    })
                array4.append(newinfoa)

    return { 
        "response": "true",
        "messages": array2,
        "message": array,
        "messagePag": array3,
        "messageApagar": array4,
    }





#-----------------DOCS FINANCEIROS/ PARCEIROS------------------- 

#GER FILE >> retornar HTML
def fetchFilePartners(id):
    arr_files = []
    ORIGIN_PATH = f"/partners/finances/{id}/NF"
    PATH = settings.BASE_DIR_DOCS + f"/partners/finances/{id}/NF" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    EXISTS = default_storage.exists(PATH) #verifica se existe >>> true or false
    if EXISTS:
        FILES = default_storage.listdir(PATH) #lista meus diretórios, nf ou outra pasta
        FILES = list(FILES)[0]
        for keys in FILES: #kyes> meu elemento dentro de files
            n = (str(((str(keys).replace("[", "")).replace("]", "")).replace("'", "")).replace(" ", "")).split(",")
            for key in n:
                key = ((str(key).replace("[", "")).replace("]", "")).replace("'", "")
                PATH_TYPE = PATH + f"/{key}"
                ORIGIN_PATH_TYPE = ORIGIN_PATH + f"/{key}"
                for fkey in default_storage.listdir(PATH_TYPE):
                    if fkey not in ["", None]:
                        fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                        try:
                            if len(fkey) > 1:
                                PATH_FILE = PATH_TYPE + f"/{fkey}"  #Caminho completo do meu documento
                                ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                arr_files.append({
                                    "type": key,
                                    "description_type": settings.LISTPATHTYPEFINANCE.get(key, ""),
                                    "file": {
                                        "name": fkey,
                                        "date_created": {
                                            "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                            "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                        },
                                        "path": ORIGIN_PATH_FILE
                                    }
                                })
                        except Exception as err:
                            print("ERRO >>>", err)


    return arr_files





#TABELAS FECHAMENTO PARCEIROS - MODAL estou aqui
def searchNotAtingeClosingPartners(request):
    id_medico = request.POST.get('id_user')
    monthCount = request.POST.get('month')
    monthF = int(datetime.now().strftime("%m"))
    
    files = fetchFilePartners(id_medico) #CHAMA A FUNÇÃO, LOCALIZA MEU DIRETÓRIO.
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f WHERE d.status_exame_f = 6 AND b.medico_resp_p = %s"
        cursor.execute(query, (id_medico,))
        dados = cursor.fetchall()
        arrayNot = []
        for paciente, agendamento, exame in dados:
            newinfoa = ({
                "paciente": paciente,
                "agendamento": convertDate(agendamento),
                "exame": exame,
                })
            arrayNot.append(newinfoa)
        
        query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f WHERE d.status_exame_f = 5 AND b.medico_resp_p = %s"
        cursor.execute(query, (id_medico,))
        dados = cursor.fetchall()
        array = []
        for pacienteG, agendamentoG, exameG in dados:
            newinfoa = ({
                "pacienteG": pacienteG,
                "agendamentoG": convertDate(agendamentoG),
                "exameG": exameG,
                })
            array.append(newinfoa)


        query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f WHERE d.status_exame_f = 2 AND b.medico_resp_p = %s"
        cursor.execute(query, (id_medico,))
        dados = cursor.fetchall()
        arrayAnalise = []
        for pacienteA, agendamentoA, exameA in dados:
            newinfoa = ({
                "pacienteA": pacienteA,
                "agendamentoA": convertDate(agendamentoA) ,
                "exameA": exameA,
                })
            arrayAnalise.append(newinfoa)


     
        queryPago = "SELECT nome_medico, nome_paciente, data_coleta, data_repasse, exame, valor_uni_partners FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_medico = %s"
        if monthCount == "" or monthCount == None:
            cursor.execute(queryPago, (monthF, id_medico,))
        else:
            cursor.execute(queryPago, (monthCount, id_medico,))
        dados = cursor.fetchall()
        arrayPago = []
        for idP, pacienteP,  dataColetaP, dataRepasseP, exameP, valor_uniP in dados:
            valor_uniP = f"R$ {valor_uniP:_.2f}"
            valor_uniP = valor_uniP.replace(".", ",").replace("_", ".")

            newinfoa = ({
                "idP": idP,
                "pacienteP": pacienteP,
                "dataColetaP": convertDate(dataColetaP),
                "dataRepasseP": convertDate(dataRepasseP),
                "exameP": exameP,
                "valor_uniP": valor_uniP,
                })
            arrayPago.append(newinfoa)


        queryCount = "SELECT COUNT(*) AS contagem, SUM(valor_uni_partners) AS total FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_medico = %s "
        if monthCount == "" or monthCount == None:
            cursor.execute(queryCount, (monthF, id_medico,))
        else:
            cursor.execute(queryCount, (monthCount, id_medico,))
        dados = cursor.fetchall()
        arrayPagoCount = []
        for contagem, valor in dados:
            valor = float(valor) if valor not in ["", None] else None
            valor = f"R$ {valor:_.2f}"
            valorS = valor.replace(".", ",").replace("_", ".")

            newinfoa = ({
                "contagem": contagem,
                "valor": valorS,
                })
            arrayPagoCount.append(newinfoa)


        queryOutros = "SELECT id_lead, nome_lead, data_regis_l, status_l FROM customer_refer.leads WHERE medico_resp_l = %s AND status_l NOT LIKE 'Paciente'"
        cursor.execute(queryOutros, (id_medico,))
        dados = cursor.fetchall()
        arrayOutros = []
        for idlead, pacienteO,  indicacaoO, statusO in dados:

            newinfoa = ({
                "idlead": idlead,
                "pacienteO": pacienteO,
                "indicacaoO": convertDate(indicacaoO),
                "statusO": statusO,
                })
            arrayOutros.append(newinfoa)

    return {
        "response": "true",
        "message": array,
        "message2": arrayNot,
        "messageAnalise": arrayAnalise,
        "messagePago": arrayPago,
        "messageCount": arrayPagoCount,
        "messageOutros": arrayOutros,
        "files": json.dumps(files),

    }




#BOTÃO CONCLUIR PAGAMENTO
def payPartnersVFunction(request):
    id_medico = request.POST.get('id_user')
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with connections['auth_finances'].cursor() as cursor:
        
        searchID = "SELECT id, nome FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        params= (date_create, id_usuario, id_medico, )

        query = "UPDATE `auth_finances`.`closing_finance` SET `status_partners` = 'Pago', `data_pag_partners` = %s, `resp_pag_partners` = %s  WHERE `nome_medico` = %s  AND  `status_partners` = 'Pendente';"
        cursor.execute(query, params)
        
    return {"response": "true", "message": "Registro financeiro atualizado."}



#INFOS DO MODAL PARCEIROS
def SearchInfoFunction(request):
    id_medico = request.POST.get('id_user')
    
    with connections['auth_finances'].cursor() as cursor:
        
        query = "SELECT b.id, b.nome, a.status_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id WHERE b.id = %s GROUP BY b.id, b.nome, a.status_partners;"
        cursor.execute(query, (id_medico,))
        dados = cursor.fetchall()
        if dados:
            for id, nome, status in dados:
                dict_response = {
                    "teste": {
                        "btn_pay": id,
                        "nome_medico": nome,
                        "status_pagamento": status,
                    },
                }
        
            return {
                "response": False if not dict_response else True,
                "message": dict_response,
            }
        



#TABELA FECHAMENTO COMERCIAL
def TableClosingCommercial(request):
    monthF = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT a.nome_comercial, b.nome, a.status_comercial, SUM(a.valor_comercial) FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_comercial = b.id WHERE MONTH( a.data_repasse) LIKE %s AND  b.nome NOT LIKE 'Tosyn Lopes' GROUP BY a.nome_comercial, b.nome, a.status_comercial, MONTH(a.data_repasse)"
        cursor.execute(query, (monthF,))
        dados = cursor.fetchall()
        array = [] 
        for id_comercial, comercial, status, valor in dados:
            valor = f"R$ {valor:_.2f}"
            valor = valor.replace(".", ",").replace("_", ".")
            newinfoa = ({
                "id": id_comercial,
                "nome": comercial,
                "status": status,
                "valor": valor
                })
            array.append(newinfoa)
        return array



#TABELA FILTRO MES FECHAMENTO COMERCIAL estou aqui
def FilterMonthClosingCommercial(request):
    month = request.POST.get('month')
    monthCount = (datetime.now().strftime("%m"))
    
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT a.nome_comercial, b.nome, a.status_comercial, SUM(a.valor_comercial) FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_comercial = b.id WHERE MONTH( a.data_repasse) LIKE %s AND b.nome NOT LIKE 'Tosyn Lopes' GROUP BY a.nome_comercial, b.nome, a.status_comercial, MONTH(a.data_repasse)"
        cursor.execute(query, (month,))
        dados = cursor.fetchall()
        array = []
        if dados:
            for idC, comercial, status, valor in dados:
                valor = (valor) if valor not in ["", None] else None
                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "idC": idC,
                    "comercial": comercial,
                    "status": status,
                    "valor": valor,
                    })
                array.append(newinfoa)
            
        querys = "SELECT COUNT(*) AS contagem, SUM(valor_comercial) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_comercial NOT LIKE 193 group by MONTH(data_repasse)"
        cursor.execute(querys, (month,))
        dados = cursor.fetchall()
        array2 = []
        if dados:
            for qdt, val, mes in dados:
                val = f"R${val:_.2f}"
                val = val.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": val,
                    "mes": mes,
                    })
                array2.append(newinfoa)

    return { 
        "response": "true",
        "messages": array2,
        "message": array,
    }


#estou aqui
#TABELA FECHAMENTO COMERCIAL - TABELAS
def searchNotAtingeClosingCommercial(request):
    id_comercial = request.POST.get('id_user')
    month = request.POST.get('month')
    monthCount = (datetime.now().strftime("%m"))

    with connections['auth_finances'].cursor() as cursor:
        query3 = "SELECT us.resp_comerce, pa.nome_p, us.nome as medico, ex.tipo_exame, ag.data_agendamento FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f WHERE us.resp_comerce = %s AND ff.status_exame_f LIKE 2"
        cursor.execute(query3, (id_comercial,))
        dados = cursor.fetchall()
        ArrayAnalise = []

        for idC, paciente, medico, exame, dataAgemdamento in dados:
            newinfoa = ({
                "idC": idC,
                "paciente": paciente,
                "medico": medico,
                "exame": exame,
                "dataAgemdamento": convertDate(dataAgemdamento) ,
                })
            ArrayAnalise.append(newinfoa)
        
        query4 = "SELECT us.resp_comerce, pa.nome_p, us.nome as medico, ex.tipo_exame, ag.data_agendamento, st.status_p FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f INNER JOIN auth_finances.status_progress st ON st.id = ff.status_exame_f WHERE us.resp_comerce = %s AND ff.status_exame_f LIKE 6 OR ff.status_exame_f LIKE 5"
        cursor.execute(query4, (id_comercial,))
        dados = cursor.fetchall()
        Glosa = []
        for idC, paciente, medico, exame, agendamento, status in dados:
            newinfoa = ({
                "idC": idC,
                "paciente": paciente,
                 "medico": medico,
                "exame": exame,
                "agendamento": convertDate(agendamento) ,
                "status": status ,
                })
            Glosa.append(newinfoa)

        
        queryP = "SELECT a.nome_comercial, a.nome_paciente, med.nome, a.data_coleta, a.data_repasse, a.exame, a.valor_comercial FROM  auth_finances.closing_finance a INNER JOIN auth_users.users med ON a.nome_medico = med.id WHERE a.nome_comercial LIKE %s AND MONTH(a.data_repasse) = %s"
        if month == "":
            cursor.execute(queryP, (id_comercial, monthCount))
     
        else:
            cursor.execute(queryP, (id_comercial, month))

        dados = cursor.fetchall()
        arrayPago = []
        for idC, paciente, medico, dataColeta, dataRepasse, exame, valor_uni in dados:
            valor_uni = f"R$ {valor_uni:_.2f}"
            valor_uni = valor_uni.replace(".", ",").replace("_", ".")
            newinfoa = ({
                "idC": idC,
                "paciente": paciente,
                "medico": medico,
                "dataColeta": convertDate(dataColeta),
                "dataRepasse": convertDate(dataRepasse),
                "exame": exame,
                "valor_uni": valor_uni,
                })
            arrayPago.append(newinfoa)
    

        query5 = "SELECT us.resp_comerce, ll.nome_lead, us.nome, ll.data_regis_l, ll.status_l FROM customer_refer.leads ll INNER JOIN auth_users.users us ON ll.medico_resp_l = us.id WHERE us.resp_comerce LIKE %s AND status_l NOT LIKE 'Paciente' ORDER BY ll.data_regis_l DESC"
        cursor.execute(query5, (id_comercial,))
        dados = cursor.fetchall()
        Outros = []
        for idC, paciente, medico, dataIndicacao, status in dados:
            newinfoa = ({
                "idC": idC,
                "paciente": paciente,
                "medico": medico,
                "dataIndicacao": convertDate(dataIndicacao) ,
                "status": status,
                })
            Outros.append(newinfoa)
        
        
    #----------------------------- aqui


    return {
        "response": "true",
        "Glosa": Glosa,
        "ArrayAnalise": ArrayAnalise,
        "arrayPago": arrayPago,
        "Outros": Outros,
    }




def SearchInfoCommercialFunction(request):
    id_comerical = request.POST.get('id_user')
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT b.id, b.nome, a.status_comercial FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_comercial = b.id WHERE b.id = %s GROUP BY b.id, b.nome, a.status_comercial;"
        cursor.execute(query, (id_comerical,))
        dados = cursor.fetchall()
        if dados:
            for id, nome, status in dados:
                dict_response = {
                    "teste": {
                        "btn_pay": id,
                        "nome_comercial": nome,
                        "status_pagamento": status,
                    },
                }
            return {
                "response": False if not dict_response else True,
                "message": dict_response
            }


#BOTÃO CONCLUIR PAGAMENTO >> COMERCIAL
def payCommercialFunction(request):
    id_comercial = request.POST.get('id_user')
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with connections['auth_finances'].cursor() as cursor:
        
        searchID = "SELECT id, nome FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        params= (date_create, id_usuario, id_comercial, )

        query = "UPDATE `auth_finances`.`closing_finance` SET `status_partners` = 'Pago', `data_pag_comercial` = %s, `resp_pag_comercial` = %s  WHERE `status_comercial` = %s  AND  `status_partners` = 'Pendente';"
        cursor.execute(query, params)
        
    return {"response": "true", "message": "Registro financeiro atualizado."}



 

 #SALVAR ANEXO
def SaveAnexoFunction(request):
    id_user = request.POST.get("id")
    type_doc = request.POST.get('type_doc')

    saveFileEditionsFinances(id_user, type_doc, request.FILES)
    files = fetchFileEditionsFinances(id)

    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar.",
                "files": json.dumps(files),

            }
            
            #FAZER UM FOR PARA REETORNAR NO JS
        
   
    return {"response": "true", "message": "Ok"
    }


#GER FILE
def fetchFileInt(id):
    arr_files = []

    ORIGIN_PATH = f"/patients/process/{id}"
    PATH = settings.BASE_DIR_DOCS + f"/patients/process/{id}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    EXISTS = default_storage.exists(PATH)
    if EXISTS:
        FILES = default_storage.listdir(PATH)
        FILES = list(FILES)[0]
        for keys in FILES:
            n = (str(((str(keys).replace("[", "")).replace("]", "")).replace("'", "")).replace(" ", "")).split(",")
            for key in n:
                key = ((str(key).replace("[", "")).replace("]", "")).replace("'", "")
                PATH_TYPE = PATH + f"/{key}"
                ORIGIN_PATH_TYPE = ORIGIN_PATH + f"/{key}"
                for fkey in default_storage.listdir(PATH_TYPE):
                    if type(fkey) != list:
                        if fkey not in ["", None]:
                            fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                            if len(fkey) > 1:
                                PATH_FILE = PATH_TYPE + f"/{fkey}"
                                ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                arr_files.append({
                                    "type": key,
                                    "description_type": settings.LISTPATHTYPE.get(key, ""),
                                    "file": {
                                        "name": fkey,
                                        "date_created": {
                                            "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                            "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                        },
                                        "path": ORIGIN_PATH_FILE
                                    }
                                })
                    else:
                        for fkey in fkey:
                            if fkey not in ["", None]:
                                fkey = ((str(fkey).replace("[", "")).replace("]", "")).replace("'", "")
                                if len(fkey) > 1:
                                    PATH_FILE = PATH_TYPE + f"/{fkey}"
                                    ORIGIN_PATH_FILE = ORIGIN_PATH_TYPE + f"/{fkey}"
                                    arr_files.append({
                                        "type": key,
                                        "description_type": settings.LISTPATHTYPE.get(key, ""),
                                        "file": {
                                            "name": fkey,
                                            "date_created": {
                                                "en": str(default_storage.get_created_time(PATH_FILE).date()),
                                                "pt": str(default_storage.get_created_time(PATH_FILE).strftime("%d/%m/%Y"))
                                            },
                                            "path": ORIGIN_PATH_FILE
                                        }
                                    })


    return arr_files


#TABELA FECHAMENTO INTERNO estou aqui
def TableClosingInt(request):
    month = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT a.nome_medico, b.nome, a.status_partners, SUM(a.valor_uni_partners) FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id WHERE a.valor_comercial LIKE '0' AND MONTH( a.data_repasse) LIKE %s GROUP BY a.nome_medico, b.nome, a.status_partners, MONTH(a.data_repasse)"
        cursor.execute(query, (month,))
        dados = cursor.fetchall()
        array = []
        for id_comercial, comercial, status, valor in dados:
            valor = f"R$ {valor:_.2f}"
            valor = valor.replace(".", ",").replace("_", ".")
            newinfoa = ({
                "id": id_comercial,
                "nome": comercial,
                "status": status,
                "valor": valor
                })
            array.append(newinfoa)
        return array


def TableClosingIntFilter(request):
    month = request.POST.get('month')
    with connections['auth_finances'].cursor() as cursor:
        params = (month,)
        query = "SELECT a.nome_medico, b.nome, a.status_partners, SUM(a.valor_uni_partners) FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id WHERE MONTH(a.data_repasse) LIKE %s AND a.valor_comercial LIKE '0' GROUP BY a.nome_medico, b.nome, a.status_partners"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        array = []
        for id_comercial, comercial, status, valor in dados:
            valor = f"R$ {valor:_.2f}"
            valor = valor.replace(".", ",").replace("_", ".")
            newinfoa = ({
                "id": id_comercial,
                "nome": comercial,
                "status": status, 
                "valor": valor
                })
            array.append(newinfoa)
            
    return{
        "response": "true", 
        "message": array
        }



#MEU FECHAMENTO FINANCEIRO
def SearchFinanceInt(request):
    with connections['auth_users'].cursor() as cursor:
        monthCount = int(datetime.now().strftime("%m"))

        searchID = "SELECT id, nome, perfil FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, perfil in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        if perfil == "7":
            queryPago = "SELECT nome_paciente, data_coleta, data_repasse, exame, valor_uni_partners FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_medico = %s"
            cursor.execute(queryPago, (monthCount, id_usuario,))
            dados = cursor.fetchall()
            array = []
            if dados in ["", None]:
                {"response": "true", "message": []}
            else:
                for pacienteP,  dataColetaP, dataRepasseP, exameP, valor_uniP in dados:
                    valor_uniP = f"R$ {valor_uniP:_.2f}"
                    valor_uniP = valor_uniP.replace(".", ",").replace("_", ".")

                    newinfoa = ({
                        "paciente": pacienteP,
                        "dataColeta": convertDate(dataColetaP),
                        "dataRepasse": convertDate(dataRepasseP),
                        "exame": exameP,
                        "valor_uni": valor_uniP,
                        })
                    array.append(newinfoa)

        elif perfil == "6": 
            queryPago = "SELECT nome_paciente, data_coleta, data_repasse, exame, valor_comercial FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_comercial = %s"
            cursor.execute(queryPago, (monthCount, id_usuario,))
            dados = cursor.fetchall()
            array = []
            for pacienteP,  dataColetaP, dataRepasseP, exameP, valor_uniP in dados:
                valor_uniP = f"R$ {valor_uniP:_.2f}"
                valor_uniP = valor_uniP.replace(".", ",").replace("_", ".")

                newinfoa = ({
                    "paciente": pacienteP,
                    "dataColeta": convertDate(dataColetaP),
                    "dataRepasse": convertDate(dataRepasseP),
                    "exame": exameP,
                    "valor_uni": valor_uniP,
                    })
                array.append(newinfoa)
        else:
            queryPago = "SELECT nome_paciente, data_coleta, data_repasse, exame, valor_uni_partners FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_comercial = %s"
            cursor.execute(queryPago, (monthCount, id_usuario,))
            dados = cursor.fetchall()
            array = []
            for pacienteP,  dataColetaP, dataRepasseP, exameP, valor_uniP in dados:
                valor_uniP = f"R$ {valor_uniP:_.2f}"
                valor_uniP = valor_uniP.replace(".", ",").replace("_", ".")

                newinfoa = ({
                    "paciente": pacienteP,
                    "dataColeta": convertDate(dataColetaP),
                    "dataRepasse": convertDate(dataRepasseP),
                    "exame": exameP,
                    "valor_uni": valor_uniP,
                    })
                array.append(newinfoa)
    return array
 

#MEU FECHAMENTO FINANCEIRO
def SearchFinanceIntAgendado(request):

    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome, perfil FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, perfil in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        if perfil == "7":
            query = "SELECT a.nome_p, b.nome_p, data_agendamento, c.tipo_exame, b.status FROM customer_refer.patients a INNER JOIN auth_agenda.collection_schedule b ON a.id_p = b.nome_p INNER JOIN admins.exam_type c ON c.id = b.tp_exame WHERE  NOT b.status LIKE  'Cancelado' AND NOT b.status LIKE 'Concluído' AND a.medico_resp_p = %s;"
            cursor.execute(query, (id_usuario,))
            dados = cursor.fetchall()
            array = []
            for pacienteA, agendamentoA, exameA in dados:
                newinfoa = ({
                    "pacienteAG": pacienteA,
                    "agendamentoAG": convertDate(agendamentoA) ,
                    "exameAG": exameA,
                    })
                array.append(newinfoa)

        elif perfil == "6": 
            query = "SELECT a.nome_p,  data_agendamento, c.tipo_exame, b.status FROM customer_refer.patients a INNER JOIN auth_agenda.collection_schedule b ON a.id_p = b.nome_p INNER JOIN admins.exam_type c ON c.id = b.tp_exame WHERE  NOT b.status LIKE  'Cancelado' AND NOT b.status LIKE 'Concluído' AND b.resp_comercial = %s;"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteA, agendamentoA, exameA,statusAG in dados:
                newinfoa = ({
                    "pacienteAG": pacienteA,
                    "agendamentoAG": convertDate(agendamentoA) ,
                    "exameAG": exameA,
                    "statusAG": statusAG,

                    })
                array.append(newinfoa)

        else:
            query = "SELECT a.nome_p, data_agendamento, c.tipo_exame, b.status FROM customer_refer.patients a INNER JOIN auth_agenda.collection_schedule b ON a.id_p = b.nome_p INNER JOIN admins.exam_type c ON c.id = b.tp_exame WHERE  NOT b.status LIKE  'Cancelado' AND NOT b.status LIKE 'Concluído' AND b.resp_comercial = %s;"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteAG, agendamentoAG, exameAG, statusAG in dados:
                newinfoa = ({
                    "pacienteAG": pacienteAG,
                    "agendamentoAG": convertDate(agendamentoAG),
                    "exameAG": exameAG,
                    "statusAG": statusAG,

                    })
                array.append(newinfoa)
    return array


#MEU FECHAMENTO FINANCEIRO
def SearchFinanceIntGlosa(request):
    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome, perfil FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, perfil in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        if perfil == "7":
            query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame, e.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f INNER JOIN auth_finances.status_progress e ON d.status_exame_f = e.id WHERE d.status_exame_f = 5 AND d.status_exame_f = 6 OR b.medico_resp_p = %s"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteG, agendamentoG, exameG, statusG in dados:
                newinfoa = ({
                    "pacienteG": pacienteG,
                    "agendamentoG": convertDate(agendamentoG) ,
                    "exameG": exameG,
                    "statusG": statusG,
                    })
                array.append(newinfoa)


        elif perfil == "6": 
            query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame, e.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f INNER JOIN auth_finances.status_progress e ON d.status_exame_f = e.id WHERE d.status_exame_f = 5 OR d.status_exame_f = 6 AND a.resp_comercial = %s;"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteG, agendamentoG, exameG, statusG in dados:
                newinfoa = ({
                    "pacienteG": pacienteG,
                    "agendamentoG": convertDate(agendamentoG) ,
                    "exameG": exameG,
                    "statusG": statusG,
                    })
                array.append(newinfoa)

        else:
            query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame, e.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f INNER JOIN auth_finances.status_progress e ON d.status_exame_f = e.id WHERE d.status_exame_f = 5 OR d.status_exame_f = 6 AND a.resp_comercial = %s"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteG, agendamentoG, exameG, statusG in dados:
                newinfoa = ({
                    "pacienteG": pacienteG,
                    "agendamentoG": convertDate(agendamentoG) ,
                    "exameG": exameG,
                    "statusG": statusG,
                    })
                array.append(newinfoa)

    return array




 
#MEU FECHAMENTO FINANCEIRO
def ClosingUnitAnalise(request):
    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome, perfil FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, perfil in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        if perfil == "7":
            query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f WHERE d.status_exame_f = 2 AND b.medico_resp_p = %s"
            cursor.execute(query, (id_usuario,))
            dados = cursor.fetchall()
            array = []
            for pacienteA, agendamentoA, exameA in dados:
                newinfoa = ({
                    "pacienteA": pacienteA,
                    "agendamentoA": convertDate(agendamentoA) ,
                    "exameA": exameA,
                    })
                array.append(newinfoa)


        elif perfil == "6": 
            query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f WHERE d.status_exame_f = 2 AND a.resp_comercial = %s"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteA, agendamentoA, exameA in dados:
                newinfoa = ({
                    "pacienteA": pacienteA,
                    "agendamentoA": convertDate(agendamentoA) ,
                    "exameA": exameA,
                    })
                array.append(newinfoa)

        else:
            query = "SELECT b.nome_p, a.data_agendamento, c.tipo_exame FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients b ON a.nome_p = b.id_p INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_finances.completed_exams d ON a.id = d.id_agendamento_f WHERE d.status_exame_f = 2 AND a.resp_comercial = %s"
            cursor.execute(query, (nome,))
            dados = cursor.fetchall()
            array = []
            for pacienteA, agendamentoA, exameA in dados:
                newinfoa = ({
                    "pacienteA": pacienteA,
                    "agendamentoA": convertDate(agendamentoA),
                    "exameA": exameA,
                    })
                array.append(newinfoa)
        return array




#MEU FECHAMENTO FINANCEIRO
def ClosingUnitResult(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome, perfil FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, perfil in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        if perfil == "7":
            
            query = "SELECT COUNT(*) AS contagem, SUM(valor_uni_partners) AS total FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_medico = %s"
            cursor.execute(query, (monthCount, id_usuario, ))
            dados = cursor.fetchall()
            array = []
            for contagem, valor in dados:
                if valor not in ["", None]:
                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "contagem": contagem,
                        "valor": valor,
                        })
                    array.append(newinfoa)


        elif perfil == "6": 
            query = "SELECT COUNT(*) AS contagem, SUM(valor_comercial) AS total FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_comercial = %s"
            cursor.execute(query, (monthCount, id_usuario, ))
            dados = cursor.fetchall()
            array = []
            for contagem, valor in dados:
                if valor not in ["", None]:
                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "contagem": contagem,
                        "valor": valor,
                        })
                    array.append(newinfoa)

        else:
            query = "SELECT COUNT(*) AS contagem, SUM(valor_uni_partners) AS total FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_medico = %s"
            cursor.execute(query, (monthCount, id_usuario, ))
            dados = cursor.fetchall()
            array = []
            for contagem, valor in dados:
                if valor not in ["", None]:
                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "contagem": contagem,
                        "valor": valor,
                        })
                    array.append(newinfoa)  
    return array





#VALOR TOTAL FECHAMENTO DOS PARCEIROS
def valTotalCommercialFunction(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        querys = "SELECT COUNT(*) AS contagem, SUM(valor_comercial) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE MONTH(data_repasse) LIKE %s AND nome_comercial NOT LIKE '193' group by MONTH(data_repasse)"
        cursor.execute(querys, (monthCount,))
        dados = cursor.fetchall()
        array2 = []
        if dados:
            for qdt, val, mes in dados:
                val = f"R${val:_.2f}"
                val = val.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "qdt": qdt,
                    "val": val,
                    "mes": mes,
                    })
                array2.append(newinfoa)
        return array2

# ------------------------------------------------------- DASHBOARD ---------------------------------------------


#DASHBOARD FINANCEIRO - REEMBOLSO -- PENDENTE
def FunctionDashPendente(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        PorcPendente = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification"
        cursor.execute(PorcPendente)
        dados = cursor.fetchall()
        porcentagemPendente = []
        if dados:
            for qdtP, regis in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "regis": regis,
                    })
                porcentagemPendente.append(newinfoa)

            QtdPendente = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE status_exame_f LIKE '8' AND identification LIKE 'Externo' group by identification"
            cursor.execute(QtdPendente)
            dados = cursor.fetchall()
            pendente = []
            if dados:
                for qdt, regis in dados:
                    percentage = (qdt * 100 /qdtP )
                    percentage= f"{percentage:_.2f} %"
                    newinfoa = ({
                        "qdt": qdt,
                        "regis": regis,
                        "percentage": percentage,
                        })
                    pendente.append(newinfoa)

            return pendente


#DASHBOARD FINANCEIRO - REEMBOLSO -- EM ANDAMENTO
def FunctionDashAndamento(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        PorcAndamento = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification"
        cursor.execute(PorcAndamento)
        dados = cursor.fetchall()
        porcentagemAndamento = []
        if dados:
            for qdtP, regis in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "regis": regis,
                    })
                porcentagemAndamento.append(newinfoa)

            QtdAndamento = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE status_exame_f LIKE '1' AND identification LIKE 'Externo' group by identification"
            cursor.execute(QtdAndamento)
            dados = cursor.fetchall()
            andamento = []
            if dados:
                for qdt, regis in dados:
                    percentage = (qdt * 100 /qdtP )
                    percentage= f"{percentage:_.2f} %"
                    newinfoa = ({
                        "qdt": qdt,
                        "regis": regis,
                        "percentage": percentage,
                        })
                    andamento.append(newinfoa)

            return andamento


#DASHBOARD FINANCEIRO - REEMBOLSO -- EM ANÁLISE
def FunctionDashAnalise(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        PorcAnalise = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification"
        cursor.execute(PorcAnalise)
        dados = cursor.fetchall()
        porcentagemAnalise = []
        if dados:
            for qdtP, regis in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "regis": regis,
                    })
                porcentagemAnalise.append(newinfoa)

            QtdAnalise = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE status_exame_f LIKE '2' AND identification LIKE 'Externo' group by identification"
            cursor.execute(QtdAnalise)
            dados = cursor.fetchall()
            analise = []
            if dados:
                for qdt, mes in dados:
                    percentage = (qdt * 100 /qdtP )
                    percentage= f"{percentage:_.2f} %"
                    newinfoa = ({
                        "qdt": qdt,
                        "mes": mes,
                        "percentage": percentage,
                        })
                    analise.append(newinfoa)

            return analise


#DASHBOARD FINANCEIRO - REEMBOLSO -- PAGO
def FunctionDashPago(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        PorcPago = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification"
        cursor.execute(PorcPago)
        dados = cursor.fetchall()
        porcentagemPago = []
        if dados:
            for qdtP, regis in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "regis": regis,
                    })
                porcentagemPago.append(newinfoa)

            QtdPago = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem,  SUM(val_pag_f), identification FROM auth_finances.completed_exams WHERE status_exame_f LIKE '4' AND identification LIKE 'Externo' group by identification"
            cursor.execute(QtdPago)
            dados = cursor.fetchall()
            pago = []
            if dados:
                for qdt, val, iden in dados:
                    percentage = (qdt * 100 /qdtP )
                    percentage= f"{percentage:_.2f} %"
                    val = f"R$ {val:_.2f}"
                    val = val.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "qdt": qdt,
                        "percentage": percentage,
                        "val": val,
                        "iden": iden,
                        })
                    pago.append(newinfoa)

                return pago



#DASHBOARD FINANCEIRO - REEMBOLSO -- OUTROS
def FunctionDashOutros(request):
    monthCount = int(datetime.now().strftime("%m"))
    with connections['auth_finances'].cursor() as cursor:
        PorcOutros = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification"
        cursor.execute(PorcOutros)
        dados = cursor.fetchall()
        porcentagemOutros = []
        if dados:
            for qdtP, regis in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "regis": regis,
                    })
                porcentagemOutros.append(newinfoa)

                QtdOutros= "SELECT COUNT(DISTINCT a.id_agendamento_f), b.status_p, a.identification FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress b ON b.id = a.status_exame_f WHERE a.status_exame_f LIKE 5 OR a.status_exame_f LIKE 6 AND a.identification LIKE 'Externo' group by b.status_p, a.identification"
                cursor.execute(QtdOutros)
                dados = cursor.fetchall()
                outros = []
                if dados:
                    for qdt, status, iden in dados:
                        percentage = (qdt * 100 /qdtP )
                        percentage= f"{percentage:_.2f} %"
                        newinfoa = ({
                            "qdt": qdt,
                            "status": status,
                            "iden": iden,
                            "percentage": percentage,
                            })
                        outros.append(newinfoa)
                        print(newinfoa)
                

                return outros



#DASHBOARD FINANCEIRO - REEMBOLSO -- TODOS EM ABERTO
def FunctionDashGeralPendente(request):
    with connections['auth_finances'].cursor() as cursor:
        PorcTotalP = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification;"
        cursor.execute(PorcTotalP)
        dados = cursor.fetchall()
        porcentagemTotalP = []
        if dados:
            for qdtP, identification in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "identification": identification,
                    })
                porcentagemTotalP.append(newinfoa)

            QtdTotalP = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, regis FROM auth_finances.completed_exams WHERE regis LIKE 0 AND identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by regis"
            cursor.execute(QtdTotalP)
            dados = cursor.fetchall()
            TotalP = []
            if dados:
                 for qdt, mes in dados:
                    percentage = (qdt * 100 /qdtP )
                    percentage= f"{percentage:_.2f} %"
                    newinfoa = ({
                        "qdt": qdt,
                        "mes": mes,
                        "percentage": percentage,
                        })
                    TotalP.append(newinfoa)

            return TotalP

#DASHBOARD FINANCEIRO - REEMBOLSO -- TODOS FINALIZADOS
def FunctionDashGeralFinalizados(request):
    with connections['auth_finances'].cursor() as cursor:
        PorcTotalF = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, identification FROM auth_finances.completed_exams WHERE identification LIKE 'Externo' AND status_exame_f NOT LIKE 9 group by identification;"
        cursor.execute(PorcTotalF)
        dados = cursor.fetchall()
        porcentagemTotalF = []
        if dados:
            for qdtP, identification in dados:
                newinfoa = ({
                    "qdtP": qdtP,
                    "identification": identification,
                    })
                porcentagemTotalF.append(newinfoa)

            QtdTotalF = "SELECT COUNT(DISTINCT id_agendamento_f) AS contagem, regis FROM auth_finances.completed_exams WHERE regis LIKE 1 AND status_exame_f NOT LIKE 9 group by regis"
            cursor.execute(QtdTotalF)
            dados = cursor.fetchall()
            TotalF = []
            if dados:
                 for qdt, mes in dados:
                    percentage = (qdt * 100 /qdtP )
                    percentage= f"{percentage:_.2f} %"
                    newinfoa = ({
                        "qdt": qdt,
                        "mes": mes,
                        "percentage": percentage,
                        })
                    TotalF.append(newinfoa)

            return TotalF



#DASHBOARD FINANCEIRO - REEMBOLSO -- CARD ALVARO
def FunctionDashCardAlvaro(request):
    with connections['auth_finances'].cursor() as cursor:
        monthCount = int(datetime.now().strftime("%m"))
        with connections['auth_finances'].cursor() as cursor:
            CardAlvaro = "SELECT COUNT(DISTINCT id_agendamento_f), SUM(val_alvaro_f), MONTH(data_registro_f) FROM auth_finances.completed_exams  val_alvaro_f WHERE MONTH(data_registro_f) LIKE %s AND identification LIKE 'Externo' AND status_exame_f != 8 group by MONTH(data_registro_f);"
            cursor.execute(CardAlvaro, (monthCount,))
            dados = cursor.fetchall()
            ArrCardAlvaro = []
            if dados:
                for qtd, val, mes in dados:
                    val = f"R$ {val:_.2f}"
                    val = val.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "qtd": qtd,
                        "val": val,
                        "mes": mes,
                        })
                    ArrCardAlvaro.append(newinfoa)

            return ArrCardAlvaro


#DASHBOARD FINANCEIRO - REEMBOLSO -- CARD WORKLAB
def FunctionDashCardWorkLab(request):
    with connections['auth_finances'].cursor() as cursor:
        monthCount = int(datetime.now().strftime("%m"))
        with connections['auth_finances'].cursor() as cursor:
            CardWorkLab = "SELECT COUNT(DISTINCT id_agendamento_f), SUM(val_work_f), MONTH(data_inc_proc_f) FROM auth_finances.completed_exams  val_alvaro_f WHERE MONTH(data_inc_proc_f) LIKE %s AND identification LIKE 'Externo' group by  MONTH(data_inc_proc_f);"
            cursor.execute(CardWorkLab, (monthCount,))
            dados = cursor.fetchall()
            ArrCardWorkLab = []
            if dados:
                for qtd, val, mes in dados:
                    val = f"R$ {val:_.2f}"
                    val = val.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "qtd": qtd,
                        "val": val,
                        "mes": mes,
                        })
                    ArrCardWorkLab.append(newinfoa)

            return ArrCardWorkLab



#DASHBOARD FINANCEIRO - REEMBOLSO -- REEMBOLSADO
def FunctionCardReembolsado(request):
    with connections['auth_finances'].cursor() as cursor:
        monthCount = int(datetime.now().strftime("%m"))
        with connections['auth_finances'].cursor() as cursor:
            CardReembolsado = "SELECT COUNT(DISTINCT id_agendamento_f), SUM(val_pag_f), MONTH(data_repasse) FROM auth_finances.completed_exams  val_alvaro_f WHERE MONTH(data_repasse) LIKE %s AND identification LIKE 'Externo' AND status_exame_f LIKE 4 group by MONTH(data_repasse);"
            cursor.execute(CardReembolsado, (monthCount,))
            dados = cursor.fetchall()
            ArrCardReembolsado = []
            if dados:
                for qtd, val, mes in dados:
                    val = f"R$ {val:_.2f}"
                    val = val.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "qtd": qtd,
                        "val": val,
                        "mes": mes,
                        })
                    ArrCardReembolsado.append(newinfoa)

            return ArrCardReembolsado



#DASHBOARD FINANCEIRO - REEMBOLSO -- TABELA MES
def FunctionDashFinanceTable(request):
    with connections['auth_finances'].cursor() as cursor:
        monthCount = int(datetime.now().strftime("%m"))
        with connections['auth_finances'].cursor() as cursor:
            Q = "SELECT conv.nome_conv, count(conv.nome_conv), MONTH(finance.data_repasse) AS mes, sum(finance.val_alvaro_f) as alvaro, sum(val_work_f)  as worklab, sum(val_pag_f) as pago FROM auth_agenda.collection_schedule ag INNER JOIN admins.health_insurance conv ON conv.id = ag.convenio INNER JOIN auth_finances.completed_exams finance ON finance.id_agendamento_f = ag.id WHERE conv.nome_conv NOT LIKE 'Cortesia Exames Autorizado ' AND MONTH(finance.data_repasse) LIKE %s AND finance.regis LIKE 1 group by conv.nome_conv, MONTH(finance.data_repasse) ORDER BY sum(finance.val_pag_f) DESC;;"
            cursor.execute(Q, (monthCount,))
            dados = cursor.fetchall()
            array = []
            if dados:
                for nome_conv, qtd, mes, alvaro, worklab, pago in dados:
                    percentage = (pago * 100 /worklab)
                    percentage= f"{percentage:_.2f} %"
                    
                    alvaro = f"R$ {alvaro:_.2f}"
                    alvaro = alvaro.replace(".", ",").replace("_", ".")

                    worklab = f"R$ {worklab:_.2f}"
                    worklab = worklab.replace(".", ",").replace("_", ".")

                    pago = f"R$ {pago:_.2f}"
                    pago = pago.replace(".", ",").replace("_", ".")

                    newinfoa = ({
                        "nome_conv": nome_conv,
                        "qtd": qtd,
                        "mes": mes,
                        "percentage": percentage,
                        "alvaro": alvaro,
                        "worklab": worklab,
                        "pago": pago,
                        })
                    array.append(newinfoa)

            return array

 


#DASHBOARD FINANCEIRO - REEMBOLSO -- TABELA ANO
def FunctionDashFinanceTableYear(request):
    with connections['auth_finances'].cursor() as cursor:
        yearCount = int(datetime.now().strftime("%Y"))
        print(yearCount)
        with connections['auth_finances'].cursor() as cursor:
            Q = "SELECT conv.nome_conv, count(conv.nome_conv), YEAR(finance.data_repasse) AS ano, sum(finance.val_alvaro_f) as alvaro, sum(val_work_f)  as worklab, sum(val_pag_f) as pago FROM auth_agenda.collection_schedule ag INNER JOIN admins.health_insurance conv ON conv.id = ag.convenio INNER JOIN auth_finances.completed_exams finance ON finance.id_agendamento_f = ag.id WHERE conv.nome_conv NOT LIKE 'Cortesia Exames Autorizado ' AND YEAR(finance.data_repasse) LIKE %s AND finance.regis LIKE 1 group by conv.nome_conv, YEAR(finance.data_repasse) ORDER BY sum(val_pag_f) DESC;"
            cursor.execute(Q, (yearCount,))
            dados = cursor.fetchall()
            array = []
            if dados:
                for nome_conv, qtd, ano, alvaro, worklab, pago in dados:
                    percentage = (pago * 100 / worklab)
                    percentage= f"{percentage:_.2f} %"
                
                    alvaro = f"R$ {alvaro:_.2f}"
                    alvaro = alvaro.replace(".", ",").replace("_", ".")

                    worklab = f"R$ {worklab:_.2f}"
                    worklab = worklab.replace(".", ",").replace("_", ".")

                    pago = f"R$ {pago:_.2f}"
                    pago = pago.replace(".", ",").replace("_", ".")

                    newinfoa = ({
                        "nome_conv": nome_conv,
                        "qtd": qtd,
                        "ano": ano,
                        "percentage": percentage,
                        "alvaro": alvaro,
                        "worklab": worklab,
                        "pago": pago,
                        })
                    array.append(newinfoa)

            return array