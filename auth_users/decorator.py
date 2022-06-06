#from asyncio.windows_events import NULL
from unicodedata import category
from django.http import QueryDict
from email import message
from email.policy import default
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
from datetime import datetime, date, timedelta
import base64
import json
import time
from re import A
from django.contrib.auth.models import User
from functions.connection.models import Connection
from functions.general.decorator import convertDate, checkDayMonth, fetchQueryUnity, fetchQueryUnityFinance
from auth_finances.functions.exams.models import saveFileEditionsFinances, FinancesExams, FinancesExamsInt, fetchFileEditionsFinances, fetchFileEditionsFinancesInt, fetchFileInt
from django.conf import settings
from django.core.files.storage import default_storage
from auth_permissions.decorator import allowPermission, json_without_success


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


#SELECT PERFIL
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

#CADASTRAR USER INTERNO
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
    unit = request.POST.get("unit")
    id_user = request.POST.get("id_user")
    data_atual = str(datetime.now().strftime('%Y-%m-%d'))

    
    with connections['auth_users'].cursor() as cursor:
        #CADASTRAR PERFIL
        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")
        
        queryExists = "SELECT id FROM auth_users.users WHERE cpf LIKE %s"
        cursor.execute(queryExists, (cpf,))
        dados = cursor.fetchall()
        if dados:
            return {"response": "true", "message": "CPF já cadastrado em sistema!"}
        else:
            param = (tp_perfil, cpf, name, date_nasc, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, cpf, data_atual, unit,)
            query = "INSERT INTO `auth_users`.`users` (`id`, `perfil`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`, `status`, `resp_comerce`, `data_regis`, `unity`, `val_padrao`, `val_porcentagem`, `val_fixo`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '', '', %s, '', 'Ativo', '193', %s, %s, '400.00', NULL, NULL);"
            cursor.execute(query, param)
            id_user = cursor.lastrowid
        #AUTENTICAÇÃO E CRIAÇÃO DE LOGIN E SENHA  aqui user   
        if User.objects.filter(username=cpf).exists():
            user = User.objects.get(username=cpf)
            user.nome = name
            user.email = email

            user.save()
        else:
           user = User.objects.create_user(username=cpf, email=email, first_name=name, last_name='', password=cpf)
         
        #PERMISSÕES PRÉ DEFINIDAS ASSIM QUE CADASTRADAS
        arrayPermission = { 
            "1": ['1','2', '3', '4', '8','9', '10','11', '12', '14', '15','16', '18','19','20','21','22', '23', '48', '49', '51', '50,' ],  #ADMINISTRADOR
            "2": ['11', '14', '22', '20', '21', '9', '8', '12', '4', '18', '23', '48'], #ATENDIMENTO (RETIRAR ALGUMAS PERMISSOES)
            "3": ["46", "16", '48'], #ENFERMAGEM
            "5": ['32','31', '26', '42', '41','39', '40', '25', '44','45', '47', '48' ], #FINANCEIRO
            "6": ['15', '16','11', '20','21', '48'], #COMERCIAL
            "7": ["20", "16", '48'], #PARCEIRO
            #"8": ['1','2', '3', '4', '8','9', '10','11', '12', '14', '15','16', '17', ], #MOTORISTA
        }
        try:
            dictP = arrayPermission[str(tp_perfil)]
        except:
            dictP = []
        
        if dictP:
            for id_permission in dictP:
                params = (
                    id_permission,
                    id_user,
                )
                query = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id_permission`, `id_user`, `nome_user`) VALUES (%s, %s, '')"
                cursor.execute(query, params)

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
    id_user = request.POST.get("id_user")
    categoria = request.POST.get("categoria")
    year = str(datetime.now().strftime("%d%Y"))
    data_atual = str(datetime.now().strftime('%Y-%m-%d'))
    padrao = request.POST.get("padrao")
    porcentagem = request.POST.get("porcentagem")
    fixo = request.POST.get("fixo")
    with connections['auth_users'].cursor() as cursor:
        padraos = padrao.replace(",", ".").replace("R$", "")
        porcentagems = porcentagem.replace("%", "")
        fixos = fixo.replace(".", "|").replace(",", ".").replace("|", "")

        padraoC = float (padraos) if padraos not in ["", None] else None
        porcentagemC = float (porcentagems) if porcentagems not in ["", None] else None
        fixoC = float (fixos) if fixos not in ["", None] else None

        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, unity in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        #CADASTRAR PERFIL
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")

        queryExists = "SELECT id FROM auth_users.users WHERE rn LIKE %s"
        cursor.execute(queryExists, (rn,))
        dados = cursor.fetchall()
        if dados:
            return {"response": "true", "message": "NC já cadastrado em sistema!"}
        else:
            param =(name, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, rn, obs, categoria, rn,id_usuario, data_atual, unity, padraoC, porcentagemC, fixoC,)
            

            query = "INSERT INTO `auth_users`.`users` ( `id`, `perfil`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`, `status`, `resp_comerce`, `data_regis`, `unity`, `val_padrao`, `val_porcentagem`, `val_fixo`) VALUES (NULL, '7', '', %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', 'Ativo', %s, %s, %s, %s, %s,%s);"
            cursor.execute(query, param)
            id_user = cursor.lastrowid
        #AUTENTICAÇÃO E CRIAÇÃO DE LOGIN E SENHA    
        if User.objects.filter(username=rn).exists():
            user = User.objects.get(username=rn)
            user.nome = rn
            user.email = email

            user.save()
        else:
           user = User.objects.create_user(username=rn, email=email, first_name=name, last_name='', password=year)
        
         #PERMISSÕES PRÉ DEFINIDAS ASSIM QUE CADASTRADAS
        arrayPermission = {
           "7":  ["20", "16",], #PARCEIRO(RETIRAR ALGUMAS PERMISSOES)
        }
        try:
            dictP = arrayPermission[str("7")]
        except:
            dictP = []
        
        if dictP:
            for id_permission in dictP:
                params = (
                    id_permission,
                    id_user,
                )
                query = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id_permission`, `id_user`, `nome_user`) VALUES (%s, %s, '')"
                cursor.execute(query, params)

    return {"response": "true", "message": "Cadastrado com sucesso!"}


#CADASTRAR INDICAÇÃO - EXTERNO
def CadastreIndication(request):
    cpf = request.POST.get("cpf")
    name = request.POST.get("name")
    email = request.POST.get("email")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    obs = request.POST.get("obs")
    convenio = request.POST.get("convenio")
    checkbox = request.POST.get("checkbox")
    data_atual = str(datetime.now().strftime('%Y-%m-%d'))
    user_resp = request.user.username

    with connections['customer_refer'].cursor() as cursor:
        params = (
            user_resp,
        )
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, params)
        dados = cursor.fetchall()
        if not dados:
            return {
                "response": "false",
                "message": "Não foi possivel cadastrar esta indicação, recarregue a página."
            }

        for id_usuario, nome, unity in dados:
            cpf = formatcpfcnpj(cpf)
            tel1 = formatTEL(tel1)
            tel2 = formatTEL(tel2)
            param = (cpf, name, email, tel1, tel2, convenio, checkbox, obs, id_usuario, id_usuario, data_atual, unity, )
            query = "INSERT INTO `customer_refer`.`leads` (`id_lead`, `cpf_lead`, `nome_lead`, `email_lead`, `tel1_lead`, `tel2_lead`, `convenio_lead`, `tp_exame`, `obs_l`, `medico_resp_l`, `resp_cadastro`, `register`, `data_regis_l`, `unity_l`, `status_l`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, %s, %s, 'Sem Contato' );"
            cursor.execute(query, param)


    return {"response": "true", "message": "Cadastrado com sucesso!"}



#CADASTRAR CONVENIO
def cadastreConv(request):
    convenio = request.POST.get("convenio")
    
    with connections['customer_refer'].cursor() as cursor:

        param =(convenio,)
        query = "INSERT INTO `admins`.`health_insurance` (`id`, `nome_conv`, `status`) VALUES (NULL,  %s, 'Ativo');"
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

@csrf_exempt
def error(request):
    raise PermissionDenied()

@csrf_exempt
def errors(request):
    response = HttpResponse('Você não possui permissão.')
    return response


#FUNCTIONS PERMISSOES
def allowPage(request, idPermission):
    login_usuario = request.user.username
    with connections['auth_permissions'].cursor() as cursor:
        query = "SELECT ap_allow.id FROM auth_permissions.auth_permissions_allow ap_allow INNER JOIN auth_users.users u ON u.id = ap_allow.id_user INNER JOIN auth_permissions.permissions_id p_i ON p_i.id = ap_allow.id_permission WHERE u.login = %s AND p_i.id_description = %s"
        params = (login_usuario, idPermission,)
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            return True
        
    return False

#SELECT ENFERMEIROS
def searchNurse(request):
    with connections['userdb'].cursor() as cursor:
        query = "SELECT id, perfil, nome FROM auth_users.users where perfil = 3 AND status = 'Ativo';"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, perfil, nome in dados:
            newinfoa = ({
                "id": id,
                "perfil": perfil,
                "nome": nome
                })
            array.append(newinfoa)

        return array


def searchDriver(request):  
    with connections['userdb'].cursor() as cursor:
        #SELECT DO BANCO DIRETO PARA O SELECT HTML >>>> TIPO DE PERFFIL
        query = "SELECT id, perfil, nome FROM auth_users.users where perfil = 8 AND status = 'Ativo';"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, perfil, nome in dados:
            newinfoa = ({
                "id": id,
                "perfil": perfil,
                "nome": nome
                })
            array.append(newinfoa)

        return array

#CONVENIO NA TABELA
def searchConvenio(request):  
    with connections['admins'].cursor() as cursor:
        query = "SELECT id, nome_conv, status FROM admins.health_insurance"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, nome_conv, status in dados:
            newinfoa = ({
                "nome_conv": nome_conv,
                "id": id,
                "status": status,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
            })
            array.append(newinfoa)
        return array
        



def searchExame(request):
    with connections['admins'].cursor() as cursor:
        query = "SELECT * FROM admins.exam_type WHERE id NOT LIKE 3 AND id NOT LIKE 5 AND id NOT LIKE 6;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, tipo_exame in dados:
            newinfoa = ({
                "tipo_exame": tipo_exame,
                "id": id
                })
            array.append(newinfoa)

        return array




#AGENDAR COLETA    
def FschedulePickup(request):
    date_age = request.POST.get("date_age")
    hr_age = request.POST.get("hr_age")
    tp_service = request.POST.get("tp_service")
    tp_exame = request.POST.get("tp_exame")
    convenio = request.POST.get("convenio")
    nurse = request.POST.get("nurse")
    driver = request.POST.get("driver")
    name = request.POST.get("name")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    doctor = request.POST.get("doctor")
    commerce = request.POST.get("commerce")
    zipcode = request.POST.get("zipcode")
    addres = request.POST.get("addres")
    number = request.POST.get("number")
    complement = request.POST.get("complement")
    district = request.POST.get("district")
    city = request.POST.get("city")
    uf = request.POST.get("uf")
    obs = request.POST.get("obs")
    val_cust = request.POST.get("cust_alv")
    val_work_lab = request.POST.get("val_w_lab")
    val_pag = request.POST.get("val_pago")
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with connections['auth_agenda'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nomeUser, unity in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        

        searchID = "SELECT A.nome_p, B.nome_p, B.unity_p FROM auth_agenda.collection_schedule A INNER JOIN customer_refer.patients B ON B.id_p = %s;"
        cursor.execute(searchID, (name,))
        dados = cursor.fetchall()
        if dados:
            for idPaciente, nomePaciente, unityPaciente in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Por favor tente novamente."
            }

        searchID = "SELECT id, nome_conv FROM admins.health_insurance WHERE nome_conv = %s"
        cursor.execute(searchID, (convenio,))
        dados = cursor.fetchall()
        
        for id_conv, nome_conv  in dados:
            params = (name, tel1, tel2, date_age, hr_age, tp_service, tp_exame, id_conv, nurse, driver, doctor, commerce, nomeUser, zipcode, addres, number,complement, district, city, uf, val_cust, val_work_lab, val_pag, obs, date_create, unityPaciente,)
            query = "INSERT INTO `auth_agenda`.`collection_schedule` (`id`, `nome_p`, `tel1_p`, `tel2_p`, `data_agendamento`, `hr_agendamento`, `tp_servico`, `tp_exame`, `convenio`, `resp_enfermeiro`, `motorista`, `resp_medico`, `resp_comercial`, `resp_atendimento`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `cidade`, `uf`, `val_cust`, `val_work_lab`, `val_pag`, `obs`, `status`, `motivo_status`, `resp_fin`, `data_fin`, `data_resgistro`, `unity`, `identification`, `perfil_int`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'Pendente', '', '', '1969-12-31', %s, %s, 'Externo', '');"
            cursor.execute(query, params)

        params2 = (name, date_create, nomeUser,)
        query2 = "INSERT INTO `customer_refer`.`register_paciente` (`id_register`, `id_pagina`, `id_paciente`, `tp_operacao`, `descrição`, `data_registro`, `user_resp`) VALUES (NULL, '2', %s, 'Coleta Agendada', 'Novo agendamento relizado.', %s, %s);"
        cursor.execute(query2, params2)
        

    return {"response": "true", "message": "Agendado com sucesso!"}



#SELECIONAR MEDICOS
def searchDoctor(request):
    with connections['userdb'].cursor() as cursor:
        query = "SELECT perfil, nome FROM auth_users.users where perfil = 7 AND status = 'Ativo';"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for perfil, nome in dados:
            newinfoa = ({
                "perfil": perfil,
                "nome": nome
                })
            array.append(newinfoa)

        return array

def searchService(request):
    with connections['admins'].cursor() as cursor:
        query = "SELECT * FROM admins.type_services;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, tipo_servico in dados:
            newinfoa = ({
                "tipo_servico": tipo_servico,
                "id": id
                })
            array.append(newinfoa)

        return array


def dealReportFilter(dictKeys, params):
    QUERY = ""

    condition = dictKeys["condition"]
    key = dictKeys["key"]
    value = dictKeys["value"]
    if key == "json":
        try:
            arrayValue = json.loads(value)
            conditionValue = condition["several"]
        except:
            arrayValue = value
            conditionValue = condition["single"]
        
        if conditionValue == "BETWEEN":
            if len(arrayValue) == 1:
                QUERY += "{} %s AND ".format(condition["single"])
                params.append(arrayValue[0])
            elif len(arrayValue) == 2:
                QUERY += "BETWEEN %s AND %s AND "
                params.append(arrayValue[0])
                params.append(arrayValue[1])

        elif conditionValue == "IN":
            if len(arrayValue) > 1:
                QUERY += "IN {} AND ".format(str(tuple(arrayValue)))
            else:
                conditionSingle = condition["single"] if condition["single"] not in ["FOR LIKE"] else "LIKE"
                QUERY += "{} %s AND ".format(conditionSingle)
                params.append(arrayValue[0]) if condition["single"] not in ["FOR LIKE"] else params.append("%" + arrayValue[0] + "%")

        else:
            conditionSingle = conditionValue if conditionValue not in ["FOR LIKE"] else "LIKE"
            QUERY += "{} %s AND ".format(conditionSingle)
            params.append(arrayValue) if conditionValue not in ["FOR LIKE"] else params.append("%" + arrayValue + "%")

    elif key == "text":
        conditionSingle = condition["single"] if condition["single"] not in ["FOR LIKE"] else "LIKE"
        QUERY += "{} %s AND ".format(conditionSingle)
        params.append(value) if condition["single"] not in ["FOR LIKE"] else params.append("%" + value + "%")

    return {
        "query": QUERY,
        "params": params
    }


#FILTRO COLETA AGENDADA
def FScheduledPickup(request):
    dictPost = json.loads(request.POST.get('search'))

    dictKeys = {
        "search_name": {
            "db": "collection_schedule cs", "columndb": "au2.nome_p", "typedb": "WHERE", "single_key": "LIKE", "several_key": "LIKE", "type_key": "text"
        },
        "search_doctor": {
            "db": "collection_schedule cs", "columndb": "cs.resp_medico", "typedb": "WHERE", "single_key": "LIKE", "several_key": "LIKE", "type_key": "text"
        },
        "search_nurse": {
            "db": "collection_schedule cs", "columndb": "cs.resp_enfermeiro", "typedb": "WHERE", "single_key": "LIKE", "several_key": "LIKE", "type_key": "text"
        },
        "search_status": {
            "db": "collection_schedule cs", "columndb": "cs.status", "typedb": "WHERE", "single_key": "LIKE", "several_key": "LIKE", "type_key": "text"
        },
        "search_service": {
            "db": "collection_schedule cs", "columndb": "cs.tp_servico", "typedb": "WHERE", "single_key": "LIKE", "several_key": "LIKE", "type_key": "text"
        },
        "search_type_exam": {
            "db": "collection_schedule cs", "columndb": "cs.tp_exame", "typedb": "WHERE", "single_key": "LIKE", "several_key": "LIKE", "type_key": "text"
        },
        "search_dt_agendamento": {
            "db": "collection_schedule cs", "columndb": "cs.data_agendamento", "typedb": "WHERE", "single_key": "=", "several_key": "BETWEEN", "type_key": "json"
        }
    }

    typeInner = {
        "auth_users.users au": ["INNER JOIN auth_users.users au ON au.id = cs.resp_enfermeiro"],
    }


    # PEGAR PERFIL E UNIDADE DO USUARIO
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT a.perfil, a.id, a.nome, a.unity FROM auth_users.users a INNER JOIN admins.units_shiloh b ON a.unity = b.id_unit_s WHERE login LIKE %s"
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

    Q = fetchQueryUnity("cs.unity", perfil, unityY)
    # VARIABLES aqui
    S_COLUMNS = ""
    S_TABLE = "auth_agenda.collection_schedule cs INNER JOIN customer_refer.patients au2 ON au2.id_p = cs.nome_p INNER JOIN auth_users.users au ON au.id = cs.resp_enfermeiro INNER JOIN admins.type_services ts ON ts.id = cs.tp_servico INNER JOIN admins.health_insurance hi ON hi.id = cs.convenio INNER JOIN admins.exam_type et ON et.id = cs.tp_exame INNER JOIN auth_users.users usrr ON usrr.nome = cs.resp_atendimento INNER JOIN admins.units_shiloh unit ON unit.id_unit_s = usrr.unity"
    S_CONDITION = "WHERE"
    S_HAVING = ""
    params = []

    for k in dictPost:
        if k in dictKeys:
            # DATABASE / TABLE
            key_table = dictKeys[k]["db"]
            inner_table = typeInner[key_table] if key_table not in "collection_schedule cs" else "auth_agenda.collection_schedule cs"
            for key_inner in inner_table:
                if key_inner not in S_TABLE:
                    S_TABLE += f" {key_inner}"
            
            # COLUMN DB
            column_table = dictKeys[k]["columndb"]
            type_condition = dictKeys[k]["typedb"]
            if type_condition == "WHERE":
                value = dealReportFilter({
                    "condition": {
                        "single": dictKeys[k]["single_key"],
                        "several": dictKeys[k]["several_key"]
                    },
                    "key": dictKeys[k]["type_key"],
                    "value": dictPost.get(k, None)
                }, params)

                params = value.get("params")
                S_CONDITION += "{} {}".format(column_table, value.get("query"))

    S_CONDITION += "{} AND ".format(Q)
    S_COLUMNS = "cs.hr_agendamento, unit.unit_s, cs.id, au2.nome_p, cs.tel1_p, ts.tipo_servico, et.tipo_exame, au.nome as resp_enfermeiro, cs.resp_medico, cs.data_agendamento, cs.status, cs.identification"
    S_CONDITION = S_CONDITION[:-5]

    db = Connection('admins', '', '', '', '')

    db.table = S_TABLE
    db.params = tuple(params)
    db.condition = "{}".format(S_CONDITION)

    arr_response = []

    try:
        dados = db.fetch([S_COLUMNS], True)
        if dados:
            for hr_agendamento, unity, id, nome_p, tel1_p, tp_servico, tp_exame, resp_enfermeiro, resp_medico, data_agendamento, status, identification in dados:
                arr_response.append({
                    "id": id,
                    "name": nome_p,
                    "tel": tel1_p, 
                    "servico": tp_servico, 
                    "exame": tp_exame,
                    "enfermeiro": resp_enfermeiro,  
                    "medico": resp_medico,
                    "unity": unity,
                    "agendamento": convertDate(data_agendamento),
                    "hr_agendamento": hr_agendamento,
                    "status": status,
                    "identification": identification
                })
    except Exception as err:
        db.condition = ""
        dados = db.fetch([S_COLUMNS], False)
        if dados:
            for hr_agendamento, unity, id, nome_p, tel1_p, tp_servico, tp_exame, resp_enfermeiro, resp_medico, data_agendamento, status, identification in dados:
                arr_response.append({
                    "id": id,
                    "unity": unity,
                    "name": nome_p,
                    "tel": tel1_p, 
                    "servico": tp_servico, 
                    "exame": tp_exame,
                    "enfermeiro": resp_enfermeiro,  
                    "medico": resp_medico,
                    "agendamento": convertDate(data_agendamento),
                    "hr_agendamento": hr_agendamento,
                    "status": status,
                    "identification": identification
                })
        

    return {
        "response": True,
        "message": arr_response
    }



#deletar convenio
def DeleteConv(request):
    nome_conv = request.POST.get("nome_conv")

    param= (nome_conv,)
    with connections['admins'].cursor() as cursor:
        query = "UPDATE `admins`.`health_insurance` SET `status` = 'Inativo' WHERE nome_conv = %s;"
        cursor.execute(query, param)
        
        return {"response": "true", "message": "Cadastro Inativo"}


#SELECT TODOS OS USUARIOS INTERNOS
def SearchUsersFull(request):
    with connections['auth_permissions'].cursor() as cursor:
        query = "SELECT a.id, a.nome, b.descriptions,  a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.descriptions NOT LIKE 'parceiro';"
        cursor.execute(query)
        dados = cursor
        array = []
        for id, nome, descriptions, status, unity in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "descriptions": descriptions,
                "status": status,
                "unity": unity,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
            })
            array.append(newinfoa)

        return array

#TABELA USUARIOS
def searchUsers(request):
    Stp_perfil = request.POST.get("Stp_perfil")
    with connections['auth_users'].cursor() as cursor:
        if Stp_perfil not in ["", None]:
            param =(Stp_perfil,)
            query = "SELECT a.id, a.nome, b.descriptions,  a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.descriptions NOT LIKE 'parceiro' AND b.id =  %s;"
            cursor.execute(query, param)
            dados = cursor.fetchall()
            array = []
            for id, nome, descriptions, status, unity in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "descriptions": descriptions,
                    "status": status,
                    "unity": unity,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                    })
                array.append(newinfoa)
            
            return {
                "message": array
            }
        else: 
            query = "SELECT a.id, a.nome, b.descriptions,  a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.descriptions NOT LIKE 'parceiro'"
            cursor.execute(query)
            dados = cursor.fetchall()
            array2 = []

        for id, nome, descriptions, status, unity in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "descriptions": descriptions,
                "status": status,
                "unity": unity,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                })
            array2.append(newinfoa)
                
        return {
            "message": array2
        }

#CHANGE STATUS > ativa e desativa
def ApiChangeStatusFunction(request):
    if not allowPermission(request, "editPartners"):
        return json_without_success("Você não possui permissão para fazer esse tipo de alteração.")

    dict_response = {} #VARIAVEL VAZIA PARA RECEBER O DICT

    try:
        id_user = int(request.POST.get('id_user'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "auth_users.users u" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE u.id = %s" #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM 
    dados = db.fetch(["u.id, u.login, u.status"], True)
    cursor = db.connection()
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for u_id, u_login, u_status in dados:
            how_status = "Inativo" if u_status.upper() == "ATIVO" else "Ativo"
            query = "UPDATE auth_users.users SET status = %s WHERE id = %s"
            params = (
                how_status,
                id_user,
            )
            cursor.execute(query, params)

            dict_response = {#aqui color
                "status": how_status,
                "btn_status": "#76c076da" if how_status.upper() == "ATIVO" else "#c74d4d"
            }

        c_status = True if how_status.upper() == "ATIVO" else False
        user = User.objects.get(username=u_login)
        user.is_active = c_status
        user.save()

    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }


#MODAL USUARIOS
def ApiViewDataUserModalFunction(request):
    dict_response = {} #VARIAVEL VAZIA PARA RECEBER O DICT

    try: 
        id_user = int(request.POST.get('id_user'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "auth_users.users u INNER JOIN auth_permissions.permissions_type b ON u.perfil = b.id"  #VAR COM CONEXAO TABLE
    db.condition = "WHERE u.id = %s" #VAR COM A CONDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM 
    dados = db.fetch(["b.descriptions, u.cpf, u.nome, u.data_nasc, u.email, u.tel1, u.tel2, u.cep, u.rua, u.numero, u.complemento, u.bairro, u.city, u.uf, u.unity"], True)
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for b_descriptions, u_cpf, u_nome, u_data_nasc, u_email, u_tel1, u_tel2, u_cep, u_rua, u_numero, u_complemento, u_bairro, u_city, u_uf, unity in dados:
            dict_response = { #VARIAVEL COM OS DICTS
                "id": id_user,
                "perfil": b_descriptions,
                "unity": unity,
                "personal": {
                    "cpfcnpj": u_cpf,
                    "name": u_nome,
                    "birthday": u_data_nasc,
                },
                "contacts": {
                    "email": u_email,
                    "phone": u_tel1,
                    "phone_aux": u_tel2,
                },
                "address": {
                    "zipcode": u_cep,
                    "street": u_rua,
                    "street_number": u_numero,
                    "complement": u_complemento,
                    "district": u_bairro,
                    "city": u_city,
                    "state": u_uf,
                }
            } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
    
    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }

    
#/////////////////////////////////////////////////////////////////////////////////////////////////////


#SELECT TODOS PARCEIROS
def searchPartiners(request):
    tp_category = request.POST.get("tp_category")
    
    with connections['auth_permissions'].cursor() as cursor:
        param = (tp_category,)
        if tp_category != "":
            query = "SELECT  a.id, a.nome, b.categoria, a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_users.Category_pertners b ON a.categoria = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.id LIKE %s AND a.status like 'Ativo' AND  a.status like 'Inativo' "
            cursor.execute(query, param)
            dados = cursor.fetchall()
            array = []

            for id, nome, categoria, status, unity in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "categoria": categoria,
                    "status": status,
                    "unity": unity,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                })
                array.append(newinfoa)
            
            return {
                "response": True,
                "message": array
            }
        else:
            query = "SELECT  a.id, a.nome, b.categoria, a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_users.Category_pertners b ON a.categoria = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.id"
            cursor.execute(query)
            dados = cursor.fetchall()
            array2 = []

            for id, nome, categoria, status, unity in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "categoria": categoria,
                    "status": status,
                    "unity": unity,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"

                    })
                array2.append(newinfoa)
                    
            return {
                "response": True,
                "message": array2
            }

#SELECT TABELA PARCEIROS
def TabelaPartners(request):
    with connections['auth_permissions'].cursor() as cursor:
        query = "SELECT  a.id, a.nome, a.rn, c.categoria, rc.nome, a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_users.Category_pertners c ON a.categoria = c.id INNER JOIN auth_users.users rc ON a.resp_comerce = rc.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, nome, rn, categoria,  resp_comercial, status, unity  in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "rn": rn,
                "categoria": categoria,
                "resp_comercial": resp_comercial,
                "status": status,
                "unity": unity,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                })
            array.append(newinfoa)

        return array

#TABELA PARCEIROS INDIVIDUAL
def TabelaPartnersUnit(request):
    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome in dados:
                pass
        else:#aqui
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        query= "SELECT  a.id, a.nome, c.categoria, a.rn, a.status, rc.nome, a.data_regis FROM auth_users.users a INNER JOIN auth_users.Category_pertners c ON a.categoria = c.id INNER JOIN auth_users.users rc ON a.resp_comerce = rc.id WHERE a.resp_comerce LIKE %s ORDER BY a.status DESC"
        params = (id_usuario,)
        cursor.execute(query, params)
        dados = cursor
        array = []
        for id, nome, categoria, rn, status, resp_comercial, data_cad in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "resp_comercial": resp_comercial,
                "categoria": categoria,
                "status": status,
                "data_cad": convertDate(data_cad),
                "rn": rn,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"

                })
            array.append(newinfoa)

        return array

    


#MODAL PARCEIROS (INFOS DO MODAL)
def ApiViewDataPartnersModalFunction(request):
    if not allowPermission(request, "editPartners"):
        return json_without_success("Você não possui permissão para fazer esse tipo de alteração.")

    dict_response = {} #VARIAVEL VAZIA PARA RECEBER O DICT
    
    try:
        id_user = int(request.POST.get('id_user'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }
    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "auth_users.users p INNER JOIN auth_users.users rc ON p.resp_comerce = rc.id" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE p.id = %s " #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM
    dados = db.fetch(["rc.nome, p.nome, p.email, p.tel1, p.tel2, p.cep, p.rua, p.numero, p.complemento, p.bairro, p.city, p.uf, p.rn, p.obs, p.categoria, p.val_padrao, p.val_porcentagem, p.val_fixo"], True)

    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for comercial, p_nome, p_email, p_tel1, p_tel2, p_cep, p_rua, p_numero, p_complemento, p_bairro, p_city, p_uf, p_rn, p_obs, p_categoria, val_padrao, val_porcentagem, val_fixo in dados:
            try:
                val_padrao = f"R$ {val_padrao:_.2f}"
                val_padrao = val_padrao.replace(".", ",").replace("_", ".")
            except:
                pass
            try:
                val_porcentagem = val_porcentagem / 100
                val_porcentagem = f" {val_porcentagem:.0%}"
                val_porcentagem = val_porcentagem.replace(".", ",").replace("_", ".")
            except:
                pass  
                    
            try:
                val_fixo = f"R$ {val_fixo:_.2f}"
                val_fixo = val_fixo.replace(".", ",").replace("_", ".")
            except:
                pass
    

        dict_response = { #VARIAVEL COM OS DICTS
            "personal": {
                "name": p_nome,
                "rn": p_rn,
                "categoria": p_categoria,
                "comercial": comercial,
            },
            "contacts": {
                "email": p_email,
                "phone": p_tel1,
                "phone_aux": p_tel2,
            },
            "address": {
                "zipcode": p_cep,
                "street": p_rua,
                "street_number": p_numero,
                "complement": p_complemento,
                "district": p_bairro,
                "city": p_city,
                "state": p_uf,
            }, 
            "obs": {
                "obs": p_obs,
            }, 
            "finances": {
                "val_padrao": val_padrao,
                "val_porcentagem": val_porcentagem,
                "val_fixo": val_fixo,
            }, 
        } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS

    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }



#MODAL PARCEIROS - MEUS PARCEIROS
def ApiViewDataPartnersModalFunctionINT(request):
    dict_response = {}
    try:
        id_user = int(request.POST.get('id_user'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }
    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "auth_users.users p" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE p.id = %s " #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM
    dados = db.fetch(["p.nome, p.email, p.tel1, p.tel2, p.cep, p.rua, p.numero, p.complemento, p.bairro, p.city, p.uf, p.rn, p.obs, p.categoria, p.val_padrao, p.val_porcentagem, p.val_fixo, p.status"], True)

    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for p_nome, p_email, p_tel1, p_tel2, p_cep, p_rua, p_numero, p_complemento, p_bairro, p_city, p_uf, p_rn, p_obs, p_categoria, val_padrao, val_porcentagem, val_fixo, status in dados:
            try:
                val_padrao = f"R$ {val_padrao:_.2f}"
                val_padrao = val_padrao.replace(".", ",").replace("_", ".")
            except:
                pass
            try:
                val_porcentagem = val_porcentagem / 100
                val_porcentagem = f" {val_porcentagem:.0%}"
                val_porcentagem = val_porcentagem.replace(".", ",").replace("_", ".")
            except:
                pass  
                    
            try:
                val_fixo = f"R$ {val_fixo:_.2f}"
                val_fixo = val_fixo.replace(".", ",").replace("_", ".")
            except:
                pass
    

        dict_response = { #VARIAVEL COM OS DICTS
            "personal": {
                "name": p_nome,
                "rn": p_rn,
                "categoria": p_categoria,
            },
            "contacts": {
                "email": p_email,
                "phone": p_tel1,
                "phone_aux": p_tel2,
            },
            "address": {
                "zipcode": p_cep,
                "street": p_rua,
                "street_number": p_numero,
                "complement": p_complemento,
                "district": p_bairro,
                "city": p_city,
                "state": p_uf,
            }, 
            "obs": {
                "obs": p_obs,
                "status": status,
            }, 
                "finances": {
                "val_padrao": val_padrao,
                "val_porcentagem": val_porcentagem,
                "val_fixo": val_fixo,
            }, 
        } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }





def ApiChangeStatusConvenioFunction(request):
    dict_response = {} #VARIAVEL VAZIA PARA RECEBER O DICT

    try:
        id_convenio = int(request.POST.get('id_convenio'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "admins.health_insurance ad" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE ad.id = %s" #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_convenio,) #VAR COM O PARAM 
    dados = db.fetch(["ad.id, ad.status"], True)
    cursor = db.connection()
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for u_id, u_status in dados:
            how_status = "Inativo" if u_status.upper() == "ATIVO" else "Ativo"
            query = "UPDATE admins.health_insurance SET status = %s WHERE id = %s"
            params = (
                how_status,
                id_convenio,
            )
            cursor.execute(query, params)

            dict_response = {
                "status": how_status,
                "btn_status": "#76c076da" if how_status.upper() == "ATIVO" else "#c74d4d"
            }

    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }

#UPDATE PARCEIROS E USUARIO INTERNO
def ApiChangeUsersModalFunction(request):
    if not allowPermission(request, "editPartners"):
        return json_without_success("Você não possui permissão para fazer esse tipo de alteração.")
        
    else:
        
        bodyData = request.POST #var para não precisar fazer tudo um por um
        print("passei aquii")

        id_user = bodyData.get('id_user')
        perfil = bodyData.get('perfil')
        padrao = bodyData.get('padrao').replace(",", ".").replace("R$", "")
        porcentagem = bodyData.get('porcentagem').replace("%", "")
        fixo = bodyData.get('fixo').replace(".", "|").replace(",", ".").replace("|", "").replace("R$", "")

        resp_commerce = bodyData.get('resp_commerce')

        padrao = float(padrao) if padrao not in ["", None] else None
        porcentagem = float(porcentagem) if porcentagem not in ["", None] else None
        fixo = float(fixo) if fixo not in ["", None] else None

        dataKeys = { #DICT PARA PEGAR TODOS OS VALORES DO AJAX
            #key, value >> valor que vem do ajax, valor para onde vai (banco de dados)
            "cpf": "cpf",
            "name": "nome",
            "date_nasc": "data_nasc",
            "email": "email",
            "tel1": "tel1",
            "tel2": "tel2",
            "zipcode": "cep",
            "addres": "rua",
            "number": "numero",
            "complement": "complemento",
            "district": "bairro",
            "city": "city",
            "uf": "uf",
            "rn": "rn",
            "categoria": "categoria",
            "obs": "obs",  
            "unity": "unity",  
        }
        print(dataKeys)
        
        db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
        cursor = db.connection()
        
        if resp_commerce == "" or resp_commerce == None:
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

            resp_commerce = id_usuario
        else:
            pass

        for key in dataKeys:
            try:
                query = "SELECT id, nome, status FROM auth_users.users where nome LIKE %s"
                cursor.execute(query, (resp_commerce,))
                dados = cursor.fetchall()
                for idC, nomeC, statusC in dados:
                    print(dados)
                    if idC != "":
                        resp_commerce = idC
                        print("1>>>>", resp_commerce)
                    
                if key in bodyData:#SE MEU VALOR DO INPUT DO AJAX EXISTIR DENTRO DO MEU POST, FAZ A QUERY
                    query = "UPDATE auth_users.users SET {} = %s, resp_comerce = %s, val_padrao = %s, val_porcentagem = %s, val_fixo = %s WHERE id = %s ".format(dataKeys[key]) #format serve para aplicar o método de formatação onde possui o valor da minha var dict e colocar dentro da minha chave, para ficar no padrão de UPDATE banco
                    params = (
                        bodyData.get(key), #serve para complementar o POST e obter o valor do input
                        resp_commerce,
                        padrao,
                        porcentagem,
                        fixo,
                        id_user,
                    )
                    cursor.execute(query, params)
            except:
                print("ERRROOO")
                query = "SELECT id FROM auth_permissions.permissions_type WHERE descriptions = %s"
                params = (
                    perfil,
                )    
                cursor.execute(query, params)
                dados = cursor.fetchall()
                for id in dados:
                    pass

                    if key in bodyData:
                        query = "UPDATE auth_users.users SET {} = %s, perfil = %s WHERE id = %s ".format(dataKeys[key])
                        params = (
                            bodyData.get(key),
                            id,
                            id_user,
                        )
                        print(params)
                        cursor.execute(query)
        return {
            "response": True,
            "message": "Dados atualizados com sucesso."
        }




#SELECT PACIENTES LISTAR
def searchIndication(request):
    with connections['customer_refer'].cursor() as cursor:
        params = (
            request.user.username,
        )

        query= "SELECT a.id_p, a.nome_p, b.nome, c.unit_s  FROM customer_refer.patients a INNER JOIN auth_users.users b ON a.medico_resp_p = b.id INNER JOIN admins.units_shiloh c ON a.unity_p = c.id_unit_s" #cortei  WHERE b.login LIKE %s
        cursor.execute(query, )
        dados = cursor
        array = []
            
        for id, nome, medico_resp, unity in dados:
            newinfoa = ({
                "nome": nome,
                "id": id,
                "medico_resp": medico_resp,
                "unity": unity,
                })
            array.append(newinfoa)

        return array


#TABELA PACIENTES INDIVIDUAL
def searchPatientsUnit(request):
    with connections['customer_refer'].cursor() as cursor:
        params = (
            request.user.username,
        )
        query= "SELECT a.id_p, a.nome_p, b.nome  FROM customer_refer.patients a INNER JOIN auth_users.users b ON a.medico_resp_p = b.id  WHERE b.login LIKE %s;"
        cursor.execute(query, params, )
        dados = cursor
        array = []
            
        for id, nome, medico_resp in dados:
            newinfoa = ({
                "nome": nome,
                "id": id,
                "medico_resp": medico_resp,
                })
            array.append(newinfoa)

        return array



#SELECT LEADS > pacientes
def searchLeads(request):
    with connections['customer_refer'].cursor() as cursor:
        query= "SELECT a.id_lead, a.nome_lead, a.cpf_lead, a.email_lead, a.tel1_lead, a.tel2_lead, a.convenio_lead, b.nome FROM customer_refer.leads a INNER JOIN auth_users.users b ON a.medico_resp_l= b.id WHERE a.register = 0" #aqui lead
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []

        for id, nome, cpf, email, phone, phone_aux, conv_medico, medico_resp in dados:
            newinfoa = ({
                "nome": nome,
                "id": id,
                "cpf": cpf,
                "email": email,
                "phone": phone,
                "phone_aux": phone_aux,
                "conv_medico": conv_medico,
                "medico_resp": medico_resp,
                
            })
            array.append(newinfoa)
        return array


#CADASTRAR PACIENTE
def ApiCadastrePatienteFunction(request):
    lead = request.POST.get("select_leads")
    data_nasc = request.POST.get("date_nasc")
    cpf = request.POST.get("cpf")
    name = request.POST.get("name")
    medico_resp = request.POST.get("medico_resp")
    email = request.POST.get("email")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    conv_medico = request.POST.get("conv_medico")
    cep = request.POST.get("zipcode")
    rua = request.POST.get("addres")
    numero = request.POST.get("number")
    complement = request.POST.get("complement")
    bairro = request.POST.get("district")
    cidade = request.POST.get("city")
    uf = request.POST.get("uf")
    obs = request.POST.get("obs")
    login = request.POST.get("login")
    senha = request.POST.get("senha")
    
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, unity in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        searchID = "SELECT medico_resp_l, nome_lead FROM customer_refer.leads WHERE id_lead = %s"
        cursor.execute(searchID, (lead,))
        dados = cursor.fetchall()
        if dados:
            for medico_resp, nome in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Lead não encontrado, tente novamente"
            }

        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
       
        queryExists = "SELECT cpf_p, id_p FROM customer_refer.patients WHERE cpf_p LIKE %s"
        cursor.execute(queryExists, (cpf,))
        dados = cursor.fetchall()
        if dados:
            queryName = "SELECT id_p FROM customer_refer.patients WHERE nome_p LIKE %s"
            cursor.execute(queryName, (name,))
            dados = cursor.fetchall()
            if dados:
                return {"response": "false", "message": "Paciente já cadastrado em sistema!"}
            else:
                param = (lead, cpf, name, email, data_nasc, tel1, tel2, cep, rua, numero ,complement, bairro, cidade, uf, conv_medico, medico_resp, id_usuario, obs, login, senha, unity,)
                query="INSERT INTO `customer_refer`.`patients` (`id_p`, `id_l_p`, `cpf_p`, `nome_p`, `email_p`, `data_nasc_p`, `tel1_p`, `tel2_p`, `cep_p`, `rua_p`, `numero_p`, `complemento_p`, `bairro_p`, `cidade_p`, `uf_p`, `convenio_p`, `medico_resp_p`, `atendente_resp_p`, `obs`, `login_conv`,`senha_conv`, `unity_p`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, param)

                #INSERIR QUANDO FIZER CADASTRO DO PACIENTE
                query= "UPDATE `customer_refer`.`leads` SET `register` = '1' WHERE (`id_lead` = %s);"
                cursor.execute(query, (lead,))
        else:
            param = (lead, cpf, name, email, data_nasc, tel1, tel2, cep, rua, numero ,complement, bairro, cidade, uf, conv_medico, medico_resp, id_usuario, obs, login, senha, unity,)
            query="INSERT INTO `customer_refer`.`patients` (`id_p`, `id_l_p`, `cpf_p`, `nome_p`, `email_p`, `data_nasc_p`, `tel1_p`, `tel2_p`, `cep_p`, `rua_p`, `numero_p`, `complemento_p`, `bairro_p`, `cidade_p`, `uf_p`, `convenio_p`, `medico_resp_p`, `atendente_resp_p`, `obs`, `login_conv`,`senha_conv`, `unity_p`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, param)

            #INSERIR QUANDO FIZER CADASTRO DO PACIENTE
            query= "UPDATE `customer_refer`.`leads` SET `register` = '1' WHERE (`id_lead` = %s);"
            cursor.execute(query, (lead,))


        return {"response": "true", "message": "Cadastrado com sucesso!"}



#SELECT CONVENIO
def SelectConvenio(request):  
    with connections['admins'].cursor() as cursor:
        query = "SELECT id, nome_conv FROM admins.health_insurance WHERE status = 'Ativo'"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, nome_conv in dados:
            newinfoa = ({
                "nome_conv": nome_conv,
                "id": id
            })
            array.append(newinfoa)

        return array

#SELECT INDICAÇÃO / LEAD / LISTAR
def searchLead(request):
    with connections['customer_refer'].cursor() as cursor:

        query= "SELECT a.nome_lead, a. data_regis_l, b.nome, c.unit_s, status_l FROM customer_refer.leads a INNER JOIN admins.units_shiloh c ON a.unity_l = c.id_unit_s INNER JOIN auth_users.users b ON a.medico_resp_l = b.id"
        cursor.execute(query)
        dados = cursor
        array = []

        for nome, data, medico_resp, unit, status in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "nome": nome,
                "data": dataFormatada,
                "unit": unit,
                "medico_resp": medico_resp,
                "status": status,
                })
            array.append(newinfoa)
        

        return array


#SELECT INDICAÇÃO INDIVIDUAL
def searchIndicationUnit(request):
    with connections['customer_refer'].cursor() as cursor:
        
        params = (
            request.user.username,
        )
        query= "SELECT a.nome_lead, a. data_regis_l, b.nome FROM customer_refer.leads a INNER JOIN auth_users.users b ON a.medico_resp_l = b.id WHERE b.login LIKE %s;"
        cursor.execute(query, params)
        dados = cursor
        array = []

        for nome, data, medico_resp in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "nome": nome,
                "data": dataFormatada,
                "medico_resp": medico_resp,
                })
            array.append(newinfoa)
        

        return array


#MODAL PACIENTES
def ApiViewDataPatientsModalFunction(request):
    dict_response = {} #VARIAVEL VAZIA PARA RECEBER O DICT

    try:
        id_user = int(request.POST.get('id_user'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "customer_refer.patients a INNER JOIN admins.health_insurance b ON b.id = a.convenio_p INNER JOIN auth_users.users d ON a.medico_resp_p = d.id INNER JOIN auth_users.users e ON a.atendente_resp_p = e.id" #VAR COM CONEEXAO TABLE
    db.condition = "WHERE a.id_p = %s" #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM
    dados = db.fetch(["a.id_p, a.id_l_p, a.cpf_p, a.nome_p, a.email_p, a.data_nasc_p, a.tel1_p, a.tel2_p, a.cep_p, a.rua_p, a.numero_p, a.complemento_p, a.bairro_p, a.cidade_p, a.uf_p, b.id, d.nome, e.nome, a.obs, a.login_conv, a.senha_conv"], True)
   
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for id_p, id_l_p, cpf_p, nome_p, email_p, data_nasc_p, tel1_p, tel2_p, cep_p, rua_p, numero_p, complemento_p, bairro_p, cidade_p, uf_p, id, nome_m, nome_a, obs_a, login_a, senha_a  in dados:
            dict_response = { #VARIAVEL COM OS DICTS
                "id_p": id_p,
                "id_lead": id_l_p,
                "personal": {
                    "name": nome_p,
                    "cpfcnpj": cpf_p,
                    "birthday": data_nasc_p
                },
                "contacts": {
                    "email": email_p,
                    "phone": tel1_p,
                    "phone_aux": tel2_p,
                },
                "address": {
                    "zipcode": cep_p,
                    "street": rua_p,
                    "street_number": numero_p,
                    "complement": complemento_p,
                    "district": bairro_p,
                    "city": cidade_p,
                    "state": uf_p,
                },  
                "med": {
                    "conv": id,
                    "name_doctor": nome_m,
                    "name_responsable": nome_a 
                    },
                "obs": {
                    "obs": obs_a,
                    "login": login_a,
                    "senha": senha_a, 
                    }
            } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
    
    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }



#UPDATE PACIENTE    
def ApiChangePatientsModalFunction(request):
    bodyData = request.POST #var para não precisar fazer tudo um por um

    id_user = bodyData.get('id_user')
    dataKeys = { #DICT PARA PEGAR TODOS OS VALORES DO AJAX
        "tp_conv": "convenio_p", #key, value >> valro que vem do ajax, valor para onde vai (banco de dados)
        "cpf": "cpf_p",
        "name": "nome_p",
        "date_nasc": "data_nasc_p",
        "email": "email_p",
        "tel1": "tel1_p",
        "tel2": "tel2_p",
        "zipcode": "cep_p",
        "addres": "rua_p",
        "number": "numero_p",
        "complement": "complemento_p",
        "district": "bairro_p",
        "city": "cidade_p",
        "uf": "uf_p",
        "obs": "obs",
        "login": "login_conv",
        "senha": "senha_conv",
    }

    db = Connection('customer_refer', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    cursor = db.connection()

    for key in dataKeys:
        if key in bodyData:#SE MEU VALOR DO INPUT DO AJAX EXISTIR DENTRO DO MEU POST, FAZ A QUERY

            query = "UPDATE customer_refer.patients SET {} = %s WHERE id_p = %s".format(dataKeys[key]) #format serve para aplicar o método de formatação onde possui o valor da minha var dict e colocar dentro da minha chave, para ficar no padrão de UPDATE banco
            params = (
                bodyData.get(key), #serve para complementar o POST e obter o valor do input
                id_user,
            )
            cursor.execute(query, params)
    return {
        "response": True,
        "message": "Dados atualizados com sucesso."
    }


def fetchHistoryPatient(id):
    try:
        id = int(id)
    except:
        return []
    
    arr_response = []

    db = Connection('customer_refer', '', '', '', '')
    db.table = "customer_refer.register_paciente history_patient INNER JOIN customer_refer.patients patients ON patients.id_p = history_patient.id_paciente" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE history_patient.id_paciente = %s"
    db.params = (
        id,
    )
    dados = db.fetch(["patients.nome_p, history_patient.id_register, history_patient.id_paciente, history_patient.tp_operacao, history_patient.descrição, history_patient.data_registro"], True)
    if dados:
        for name_patient, id_r, id_patient, type_operation, description, date_register in dados:
            date_register = str(datetime.strptime(str(date_register), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S"))
            arr_response.append({
                "id": id_r,
                "patient_id": id_patient,
                "patient_name": name_patient,
                "type_operation": type_operation,
                "description": description,
                "date_register": date_register,
            })

    return arr_response


def FetchPatientsFilesFunction(bodyData): #aqi
    try:
        keysLIST = []
        id = bodyData.id_user
        PATH = settings.BASE_DIR_DOCS + f"/patients/process/{id}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
        PATH_ORIGIN = f"/patients/process/{id}"
        DS = default_storage
        if DS.exists(PATH):
            LIST_TYPES = DS.listdir(PATH)
            if LIST_TYPES:
                if len(LIST_TYPES) > 0:
                    arrLIST = []
                    for key in LIST_TYPES[0]:
                        arrLIST.append(key)

                    if arrLIST:
                        for paths in arrLIST:
                            arrLISTPATHS = DS.listdir(f"{PATH}/{paths}")
                            for key in arrLISTPATHS[1]:
                                keysLIST.append({
                                    "type": str(paths),
                                    "type_desc": settings.LISTPATHTYPE.get(str(paths), ""),
                                    "name": key,
                                    "path": PATH_ORIGIN + f"/{paths}/{key}",
                                    "date_create": {
                                        "en": str(default_storage.get_created_time(f"{PATH}/{paths}/{key}").date()),
                                        "pt": str(default_storage.get_created_time(f"{PATH}/{paths}/{key}").strftime("%d/%m/%Y"))
                                    },
                                    "url": settings.SHORT_PLATAFORM + f"/docs/patients/process/{id}/{paths}/{key}"
                                })

        return {
            "response": True,
            "message": {
                "docs": keysLIST,
                "history": fetchHistoryPatient(id)
            }
        }
    except Exception as err:
        return {
            "response": False,
            "message": "Não foi possível encontrar este paciente."
        }


def DeletePatientsFilesFunction(request):
    bodyData = QueryDict(request.body.decode(), mutable=True)

    PATH = settings.BASE_DIR_DOCS + bodyData.get('path')
    if default_storage.exists(PATH):
        default_storage.delete(PATH)
        if not default_storage.exists(PATH):
            return {
                "response": True,
                "message": "Arquivo excluido com sucesso."
            }

    return {
        "response": False,
        "message": "Não foi possível excluir este arquivo."
    }


#AGENDAR COLETA SELECT2 LEADS
def SearchSelectSchedule(request):
    with connections['customer_refer'].cursor() as cursor:
        #query= "SELECT a.id_p, a.cpf_p, a.nome_p, a.tel1_p, a.tel2_p, a.cep_p, a.rua_p, a.numero_p, a.complemento_p, a.bairro_p, a.cidade_p, a.uf_p, c.nome, d.nome FROM customer_refer.patients a INNER JOIN auth_users.users d ON a.atendente_resp_p = d.id INNER JOIN auth_users.users c ON a.medico_resp_p = c.id"
        query= "SELECT a.id_p, a.cpf_p, a.nome_p, a.tel1_p, a.tel2_p, a.cep_p, a.rua_p, a.numero_p, a.complemento_p, a.bairro_p, a.cidade_p, a.uf_p, med.nome as medico, co.nome_conv, comm.nome FROM customer_refer.patients a INNER JOIN auth_users.users med ON a.medico_resp_p = med.id INNER JOIN admins.health_insurance co ON a.convenio_p = co.id INNER JOIN auth_users.users comm ON med.resp_comerce = comm.id"
        cursor.execute(query) 
        dados = cursor
        array = []
        for id, cpf, nomep, tel1, tel2, cep, rua, numero, complemento, bairro, cidade, uf, nome_med, convenio, nome_commerce  in dados:
            
            if nome_commerce != "Tosyn Lopes":
                newinfoa = ({
                    "id_p": id,
                    "nome_p": nomep,
                    "cpf_p": cpf,
                    "tel1": tel1,
                    "tel2": tel2,
                    "cep": cep,
                    "rua": rua,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "uf": uf,
                    "nome_med": nome_med,
                    "convenio": convenio,
                    "nome_commerce": nome_commerce,
                    })
                array.append(newinfoa)

            else:
                newinfoa = ({
                    "id_p": id,
                    "nome_p": nomep,
                    "cpf_p": cpf,
                    "tel1": tel1,
                    "tel2": tel2,
                    "cep": cep,
                    "rua": rua,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "uf": uf,
                    "nome_med": nome_med,
                    "convenio": convenio,
                    })
                array.append(newinfoa)
        return array #pega os valores


#TABELA COLETA AGENDADA TODOS OS AGENDAMENTOS
def searchScheduledPickup(request):
    dt_now = checkDayMonth("this_month")
    dt_start = dt_now["dt_start"]
    dt_end = dt_now["dt_end"]

    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT a.perfil, a.id, a.nome, a.unity FROM auth_users.users a INNER JOIN admins.units_shiloh b ON a.unity = b.id_unit_s WHERE login LIKE %s"
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

        Q = fetchQueryUnity("unit.id_unit_s", perfil, unityY) 
        query = "SELECT unit.unit_s, a.id, pa.nome_p, a.tel1_p, b.tipo_servico, c.tipo_exame, e.nome, a.resp_medico, a.data_agendamento, a.status, a.hr_agendamento FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_users.users usrr ON usrr.nome = a.resp_atendimento INNER JOIN admins.units_shiloh unit ON unit.id_unit_s = usrr.unity WHERE {} AND a.status IN ('Pendente', 'Em Andamento') AND a.identification LIKE  'Externo'  ORDER BY a.data_agendamento ASC".format(Q)
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []

        for unity, id, paciente, phone, service, exame, nurse, doctor, data, status, hr_age  in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "id": id,
                "unity": unity,
                "paciente": paciente,
                "phone": phone,
                "service": service,
                "exame": exame,
                "nurse": nurse,
                "hr_age": hr_age,
                "date_age": dataFormatada,
                "status": status,
                })
            array.append(newinfoa)
    return array 

#MODAL COLETA AGENDADA
def SearchModalScheduled(request):
    id = request.POST.get('id_user')
    dict_response = {}

    files = fetchFileEditionsFinances(id)

    with connections['customer_refer'].cursor() as cursor:
        params = (
            id,
        )
        query = "SELECT a.id, a.data_agendamento, a.hr_agendamento, b.tipo_servico, c.tipo_exame, g.nome_conv, jj.id as id_enfermeira, e.nome, jm.nome, np.nome_p, a.tel1_p, a.tel2_p, a.resp_medico, a.resp_atendimento, a. resp_comercial, a.cep, a.rua, a.numero, a.complemento, a.bairro, a.cidade, a.uf, a.val_cust, a.val_work_lab, a.val_pag, a.obs, b.tipo_servico, c.tipo_exame, a.status, a.motivo_status, co.color FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN admins.health_insurance g ON a.convenio = g.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN admins.status_colors co ON a.status = co.status_c INNER JOIN customer_refer.patients np ON a.nome_p = np.id_p INNER JOIN auth_users.users jj ON e.nome = jj.nome INNER JOIN auth_users.users jm ON a.motorista = jm.id WHERE a.id = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for a_id, a_data_agendamento, a_hr_agendamento, b_tipo_servico, c_tipo_exame, g_nome_conv, jj_id, e_nome, jm_nome, np_nome_p, a_tel1_p, a_tel2_p, a_resp_medico, a_resp_atendimento, a_resp_comercial, a_cep, a_rua, a_numero, a_complemento, a_bairro, a_cidade, a_uf, a_val_cust, a_val_work_lab, a_val_pag, a_obs, b_tipo_servico, c_tipo_exame, a_status, a_motivo_status, co_color in dados:
                dict_response = {
                    "agendamento": {
                        "data_agendamento": a_data_agendamento,
                        "hr_agendamento": a_hr_agendamento,
                        "tipo_servico": b_tipo_servico,
                        "tipo_exame": c_tipo_exame,
                        "motorista": jm_nome,
                        "nurse": jj_id,
                        "NomeNurse": e_nome,
                        "convenio": g_nome_conv,
                        "doctor": a_resp_medico,
                        "commerce": a_resp_comercial,
                        "id": a_id,
                        "motoristaNome": jm_nome,
                        
                    },
                    "pessoal": {
                        "phone1": a_tel1_p,
                        "phone2": a_tel2_p,
                        "paciente": np_nome_p,
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
                    },
                    "obs": {
                        "obs": a_obs,
                        "statusM": a_status,
                        "motivo_status": a_motivo_status,
                        "color": co_color,


                    },
                "files": json.dumps(files),
                } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
    
    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }


#ATUALIZAR STATUS DO AGENDAMENTO CONCLUIDO
def FunctionStatusAgendaConc(request):
    id = request.POST.get("id")
    convenio = request.POST.get("convenio")
    data_atual = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
   
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
                "message": "Login expirado, faça login novamente para continuar."
            }

        param= (id_usuario, data_atual, id,)
        param2= ( id, data_atual,)
        query = "UPDATE `auth_agenda`.`collection_schedule` SET `status` = 'Concluído', `resp_fin` = %s, data_fin = %s WHERE (`id` = %s);"
        cursor.execute(query, param)
        
        paramver = (id,)
        queryver  = "SELECT tp_servico, id, convenio from auth_agenda.collection_schedule where id LIKE %s"
        cursor.execute(queryver, paramver)
        dados = cursor.fetchall()
        for tp_serviço, id, conv in dados:
            if  tp_serviço != 5:
                if conv !=  '72':
                    queryVerif = "SELECT id, id_agendamento_f FROM auth_finances.completed_exams WHERE id_agendamento_f LIKE %s "
                    cursor.execute(queryVerif, (id,))
                    dados = cursor.fetchall()
                    if dados:
                        for id, idagendamento in dados:
                            return {
                            "response": "true", 
                            "message": "Coleta já concluída."
                            }
                    else:
                        pass
                        query2 = "INSERT INTO `auth_finances`.`completed_exams` (`id`, `id_agendamento_f`, `data_inc_proc_f`, `status_exame_f`, `resp_inicio_p_f`, `val_alvaro_f`, `val_work_f`, `val_pag_f`, `porcentagem_paga_f`, `data_repasse`, `nf_f`, `anx_f`, `data_aquivo_f`, `data_final_f`, `data_registro_f`, `resp_final_p_f`, `regis`, `obs_f`, `identification`, `def_glosado_n_atingido`) VALUES (NULL, %s, NULL, '8', NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0', NULL, NULL, %s, NULL, '0', NULL, 'Externo', NULL);"
                        cursor.execute(query2, param2)
        params7=(id,)
        searchID2 = "SELECT id, nome_p FROM auth_agenda.collection_schedule WHERE id LIKE %s"
        cursor.execute(searchID2, params7)
        dadoss = cursor.fetchall()
        if dadoss:
            for idc, id_paciente in dadoss:
                pass

                params3 = (id_paciente, data_atual, data_atual, nome,)
                query3 = "INSERT INTO `customer_refer`.`register_paciente` (`id_register`, `id_pagina`, `id_paciente`, `tp_operacao`, `descrição`, `data_registro`, `user_resp`) VALUES (NULL, '2', %s, 'Coleta Concluída', 'Finalizado dia: ' %s, %s, %s);"
                cursor.execute(query3, params3)
        
        return {"response": "true", "message": "Agendamento Concluído com sucesso!"}


#REGAENDAR
def ApiReagendarAgendaConcFunction(request):
    id = request.POST.get("id")
    data_agendar = request.POST.get("data_agendar")
    hr_age = request.POST.get("hr_age")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    zipcode = request.POST.get("zipcode")
    addres = request.POST.get("addres")
    number = request.POST.get("number")
    complement = request.POST.get("complement")
    district = request.POST.get("district")
    city = request.POST.get("city")
    uf = request.POST.get("uf")
    cust_alv = request.POST.get("cust_alv")
    obs = request.POST.get("obs")
    motivo_status = request.POST.get("motivo_status")
    nurse = request.POST.get("nurse")
    data_atual = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with connections['auth_agenda'].cursor() as cursor:
        params = (
            tel1, tel2, data_agendar,  hr_age, nurse, zipcode, addres, number, complement, district, city, uf, cust_alv, obs, motivo_status, data_atual, id,
        )
        #query = "UPDATE auth_agenda.collection_schedule SET data_agendamento = %s WHERE id = %s"
        query = "UPDATE `auth_agenda`.`collection_schedule` SET `tel1_p` = %s, `tel2_p` = %s, `data_agendamento` = %s, `hr_agendamento` = %s, `resp_enfermeiro` = %s, `cep` = %s, `rua` = %s, `numero` = %s, `complemento` = %s, `bairro` = %s, `cidade` = %s, `uf` = %s, `val_cust` = %s, `obs` = %s, `status` = 'Pendente', motivo_status = 'Reagendado - ' %s,  data_fin = %s  WHERE (`id` = %s);"
        cursor.execute(query, params)

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

        params7=(id,)
        searchID2 = "SELECT id, nome_p FROM auth_agenda.collection_schedule WHERE id LIKE %s"
        cursor.execute(searchID2, params7)
        dadoss = cursor.fetchall()
        if dadoss:
            for idc, id_paciente in dadoss:
                pass

        params2 = (id_paciente, motivo_status, data_atual, nome)
        query2 = "INSERT INTO `customer_refer`.`register_paciente` (`id_register`, `id_pagina`, `id_paciente`, `tp_operacao`, `descrição`, `data_registro`, `user_resp`) VALUES (NULL, '2', %s, 'Coleta Reagendada', 'Motivo: ' %s, %s, %s);"
        cursor.execute(query2, params2)
    return {
        "response": "true",
        "message": "Reagendado com sucesso."
    }



    #ATUALIZAR STATUS FRUSTRAR
def FunctionStatusAgendaFrustrar(request):
    id = request.POST.get("id")
    motivo_status = request.POST.get("motivo_status")
    data_atual = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
                "message": "Login expirado, faça login novamente para continuar."
            }
        param= (id_usuario, data_atual, motivo_status, id,)

        query = "UPDATE auth_agenda.collection_schedule SET status = 'Frustrado', resp_fin = %s, data_fin = %s, motivo_status = %s WHERE id = %s;"
        cursor.execute(query, param)

        
        params7=(id,)
        searchID2 = "SELECT id, nome_p FROM auth_agenda.collection_schedule WHERE id LIKE %s"
        cursor.execute(searchID2, params7)
        dadoss = cursor.fetchall()
        if dadoss:
            for idc, id_paciente in dadoss:
                pass
        
        params2 = (id_paciente, motivo_status, data_atual, nome,)
        query2 = "INSERT INTO `customer_refer`.`register_paciente` (`id_register`, `id_pagina`, `id_paciente`, `tp_operacao`, `descrição`, `data_registro`, `user_resp`) VALUES (NULL, '2', %s, 'Coleta Frustrada', 'Motivo: ' %s, %s, %s);"
        cursor.execute(query2, params2)
    #"true" -> STRING
    #true -> BOOLEAN
    return {"response": "true", "message": "Ok"}

    
#ATUALIZAR STATUS CANCELAR
def FunctionStatusAgendaCancel(request):
    id = request.POST.get("id")
    motivo_status = request.POST.get("motivo_status")
    data_atual = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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
                "message": "Login expirado, faça login novamente para continuar."
            }
        
        param= (id_usuario, data_atual, motivo_status, id,)

        query = "UPDATE auth_agenda.collection_schedule SET status = 'Cancelado', resp_fin = %s, data_fin = %s, motivo_status = %s WHERE id = %s;"
        cursor.execute(query, param)


        params7=(id,)
        searchID2 = "SELECT id, nome_p FROM auth_agenda.collection_schedule WHERE id LIKE %s"
        cursor.execute(searchID2, params7)
        dadoss = cursor.fetchall()
        if dadoss:
            for idc, id_paciente in dadoss:
                pass
        
        params2 = (id_paciente, motivo_status, data_atual, nome,)
        query2 = "INSERT INTO `customer_refer`.`register_paciente` (`id_register`, `id_pagina`, `id_paciente`, `tp_operacao`, `descrição`, `data_registro`, `user_resp`) VALUES (NULL, '2', %s, 'Coleta Cancelada', 'Motivo: '%s, %s, %s);"
        cursor.execute(query2, params2)
    #"true" -> STRING
    #"true" -> STRING
    #true -> BOOLEAN
    
    return {"response": "true", "message": "Ok"}



#SELECT STATUS
def FunctionStatusSelect(request):
    with connections['admins'].cursor() as cursor:
        query = "SELECT id_c, status_c FROM admins.status_colors;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, status in dados:
            newinfoa = ({
                "id": status,
                "status": status,
                
                })
            array.append(newinfoa)
    return array


#TABELA SELECT AGENDADOS CONCLUIDOS 
def searchConcluidosF(request):
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

        if perfil == "1":
            query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_agendamento, ex.tipo_exame, spa.status_p, uni.unit_s, id_unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN admins.units_shiloh uni ON pa.unity_p = uni.id_unit_s INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' and spa.status_p NOT LIKE 'Glosa' and spa.status_p NOT LIKE 'Valor Não Atingido' AND a.identification LIKE 'Externo' ORDER BY a.data_agendamento ASC"
            cursor.execute(query)
            dados = cursor
            array = []
                
            for id, paciente, comercial, medico, dataconc, exame, status_p, unidade, id_unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "comercial": comercial,
                    "medico": medico,
                    "dataconc": convertDate(dataconc),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    "id_unidade": id_unidade,
                    })
                array.append(newinfoa)
        else:
            query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_agendamento, ex.tipo_exame, spa.status_p, uni.unit_s, id_unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN admins.units_shiloh uni ON pa.unity_p = uni.id_unit_s INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id WHERE uni.id_unit_s like %s AND a.status = 'Concluído' AND sp.regis LIKE  '0' and spa.status_p NOT LIKE 'Glosa' and spa.status_p NOT LIKE 'Valor Não Atingido' AND a.identification LIKE 'Externo' ORDER BY a.data_agendamento ASC"
            cursor.execute(query, (unityY,))
            dados = cursor
            array = []
                
            for id, paciente, comercial, medico, dataconc, exame, status_p, unidade, id_unidade in dados:
                newinfoa = ({
                    "id": id,
                    "paciente": paciente,
                    "comercial": comercial,
                    "medico": medico,
                    "dataconc": convertDate(dataconc),
                    "exame": exame,
                    "status_p": status_p,
                    "unidade": unidade,
                    "id_unidade": id_unidade,
                    })
                array.append(newinfoa)
    return array


#SELECT STATUS PROCESSO
def FunctionStatus(request):
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT id, status_p FROM auth_finances.status_progress WHERE id NOT LIKE '7' ORDER BY status_p;"
        cursor.execute(query)
        dados = cursor
        array = []
        for id, status in dados:
            newinfoa = ({
                "id": id,
                "status": status,
                })
            array.append(newinfoa)
    return array


#TIPO DE ANEXO
def FunctionSearchTypeAnexo(request):
    with connections['admins'].cursor() as cursor:
        query = "SELECT * FROM admins.tp_anx;"
        cursor.execute(query)
        dados = cursor
        array = []
        
        for id, tipo_anexo in dados:
            newinfoa = ({
                "id": id,
                "tipo_anexo": tipo_anexo,
                })
            array.append(newinfoa)
    return array

#INICIO DO PROCESSO REEMBOLSO
def FunctionStartProcess(request):
    
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    date_create_ptbr = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    idq = request.POST.get("id_user")
    status = request.POST.get("statusProgresso")

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

        param = (date_create, id_usuario, idq,)
        query = "UPDATE `auth_finances`.`completed_exams` SET `data_inc_proc_f` = %s, `status_exame_f` = '1', `resp_inicio_p_f` = %s WHERE (`id_agendamento_f` = %s);"
        cursor.execute(query, param)
        
        param2 = (idq, nome, date_create,)
        query2 = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `id_agendamento`, `tp_operacao`, `nome_user`, `descricao`, `data_operacao`) VALUES (NULL, '1', %s, 'Iniciar Processo',  %s, 'Usuario iniciou o processo para reembolso', %s);"
        cursor.execute(query2, param2)
        
        return {
            "response": "true",
            "message": "Processo Financeiro iniciado!", 
            "dadoss": {
                "date_first": date_create_ptbr,
                "statusProgresso": "1"
            }
        }
    

#MODAL COLETA AGENDADA CONCLUIDA kkk
def SearchModalExamsFunction(request):
    id = request.POST.get('id_user')
    
    FC = FinancesExams()
    dict_response = {}
    finances_exams_data = FC.fetch_exams(id)

    modal_data = FC.schedule_collection(id)

    dict_response.update(modal_data) if modal_data else None
    dict_response.update(finances_exams_data) if modal_data else None

    #dict_response["history"] = historicExamConclFunction(id)
    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MESSAGE COM O DICT 
    }

#LISTAR TODOS OS LEADS QUE ENTRAM
def SearchLeadsAll(request):
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dadosU = cursor.fetchall()
        if dadosU:
            for id_usuarioU, nomeU, unity in dadosU:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        query= "SELECT a.id_lead, a.nome_lead, a.tel1_lead, a.data_regis_l, b.nome, a.unity_l, status_l FROM customer_refer.leads a INNER JOIN auth_users.users b ON a.medico_resp_l = b.id  WHERE a.register = 0 AND status_l = 'Sem Contato' AND a.unity_l = %s ORDER BY a.data_regis_l desc"
        cursor.execute(query, (unity,))
        dados = cursor
        array = []

        for id, nome, telefone, data, medico_resp, unity, status in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "id": id,
                "nome": nome,
                "telefone": telefone,
                "data": dataFormatada,
                "medico_resp": medico_resp,
                "nomeU": nomeU,
                "status": status,
                })
            array.append(newinfoa)
        

        return array

#SELECT MÉDICOS
def searchDoctorLead(request):
    with connections['userdb'].cursor() as cursor:
        query = "SELECT id, nome FROM auth_users.users ;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, nome in dados:
            newinfoa = ({
                "id": id,
                "nome": nome
                })
            array.append(newinfoa)
        return array


        
#CADASTRAR LEAD INTERNO
def CadastreLead(request):
    doctor = request.POST.get("doctor")
    cpf = request.POST.get("cpf")
    name = request.POST.get("name")
    email = request.POST.get("email")
    tel1 = request.POST.get("tel1")
    tel2 = request.POST.get("tel2")
    obs = request.POST.get("obs")
    convenio = request.POST.get("convenio")
    checkbox = request.POST.get("checkbox")
    data_atual = str(datetime.now().strftime('%Y-%m-%d'))
    
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nome, unity in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        param =(cpf, name, email, tel1, tel2, convenio, checkbox, obs, doctor, data_atual, unity)
        query = "INSERT INTO `customer_refer`.`leads` (`id_lead`, `cpf_lead`, `nome_lead`, `email_lead`, `tel1_lead`, `tel2_lead`, `convenio_lead`, `tp_exame`, `obs_l`, `medico_resp_l`, `resp_cadastro`, `register`, `data_regis_l`, `unity_l`, `status_l` ) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '0', %s, %s, 'Sem Contato');"
        cursor.execute(query, param)
    return {"response": "true", "message": "Cadastrado com sucesso!"}



#ATUALIZAR CADASTRO INTERNO
def UpdatePerfil(request):
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
    id_user = request.POST.get("id_user")
    
    with connections['auth_users'].cursor() as cursor:
        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")
        
        queryExists = "SELECT id FROM auth_users.users WHERE cpf LIKE %s"
        cursor.execute(queryExists, (cpf,))
    
        param2 = (tp_perfil, cpf, name, date_nasc, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, id_user,)
        query2 = "UPDATE users SET perfil = %s, cpf = %s, nome = %s, data_nasc = %s, email = %s, tel1 = %s, tel2 = %s, cep = %s, rua = %s, numero = %s, complemento = %s, bairro = %s, city = %s, uf = %s WHERE id = %s"
        cursor.execute(query2, param2)

    return {"response": "true", "message": "Cadastrado atualizado com sucesso!"}


#GET FILE REMOVE >>>
def ModalExamsFinanceFileRemoveFunction(request):
    id_patient = request.POST.get('id_patient')
    type_file = request.POST.get('type_file')
    id_file = request.POST.get('id_file')

    try:
        id_patient = int(id_patient)
        type_file = int(type_file)
    except:
        return {
            "response": "false",
            "message": "Não foi possível encontrar este arquivo."
        }
    
    PATH = settings.BASE_DIR_DOCS + f"/patients/process/{id_patient}/{type_file}/{id_file}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    if default_storage.exists(PATH):
        try:
            default_storage.delete(PATH)
            if not default_storage.exists(PATH):
                return {
                    "response": "true",
                    "message": "Arquivo excluido com sucesso."
                }
        except:
            pass

    else:
        return {
            "response": "true",
            "message": "Arquivo excluido com sucesso."
        }
    
    return {
        "response": "false",
        "message": "Não foi possível encontrar ou remover este arquivo."
    } 





#GET FILE REMOVE
def ModalExamsFinanceFileRemoveFunctionInt(request):
    id_patient = request.POST.get('id_patient')
    type_file = request.POST.get('type_file')
    id_file = request.POST.get('id_file')

    try:
        id_patient = int(id_patient)
        type_file = int(type_file)
    except:
        return {
            "response": "false",
            "message": "Não foi possível encontrar este arquivo."
        }
    
    PATH = settings.BASE_DIR_DOCS + f"/user/process/{id_patient}/{type_file}/{id_file}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    if default_storage.exists(PATH):
        try:
            default_storage.delete(PATH)
            if not default_storage.exists(PATH):
                return {
                    "response": "true",
                    "message": "Arquivo excluido com sucesso."
                }
        except:
            pass
    else:
        return {
            "response": "true",
            "message": "Arquivo excluido com sucesso."
        }
    
    return {
        "response": "false",
        "message": "Não foi possível encontrar ou remover este arquivo."
    } 



#CADASTRAR UNIDADE
def cadastreUnit(request):
    unit = request.POST.get("newunit")
    
    with connections['admins'].cursor() as cursor:
        param =(unit,)
        query = "INSERT INTO `admins`.`units_shiloh` (`id_unit_s`, `unit_s`, `status_s`) VALUES (NULL,  %s, 'Ativo');"
        cursor.execute(query, param)
        
    return {"response": "true", "message": "Cadastrado com sucesso!"}

    

def ApiChangeStatusUnitFunction(request):
    dict_response = {}

    try:
        id_unit = int(request.POST.get('id_unit'))
    except:
        return {
            "response": False,
            "message": "Nenhuma Unidade encontrado com este id."
        }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "admins.units_shiloh ad" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE ad.id_unit_s = %s" #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_unit,) #VAR COM O PARAM 
    dados = db.fetch(["ad.id_unit_s, ad.status_s"], True)
    cursor = db.connection()
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for u_id, u_status in dados:
            how_status = "Inativo" if u_status.upper() == "ATIVO" else "Ativo"
            query = "UPDATE admins.units_shiloh SET status_s = %s WHERE id_unit_s = %s"
            params = (
                how_status,
                id_unit,
            )
            params
            cursor.execute(query, params)

            dict_response = {
                "status": how_status,
                "btn_status": "#76c076da" if how_status.upper() == "ATIVO" else "#c74d4d"
            }

    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }

#UNIDADE NA TABELA
def searchUnidadeTabela(request):  
    with connections['admins'].cursor() as cursor:
        query = "SELECT id_unit_s, unit_s, status_s FROM admins.units_shiloh;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id_unit_s, unit_s, status_s in dados:
            newinfoa = ({
                "id": id_unit_s,
                "nome": unit_s,
                "status": status_s,
                "btn_status": "#76c076da" if status_s.upper() == "ATIVO" else "#c74d4d"
            })
            array.append(newinfoa)
        return array
        


def searchUnit(request):
    with connections['admins'].cursor() as cursor:
        #SELECT DO BANCO DIRETO PARA O SELECT HTML >>>> TIPO DE PERFFIL
        query = "SELECT id_unit_s, unit_s FROM admins.units_shiloh;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id_unit_s, unit_s in dados:
            newinfoa = ({
                "id_unit_s": id_unit_s,
                "unit_s": unit_s
                })
            array.append(newinfoa)

        return array

#--------------------------------------------------------------------------------------------------------------------

#DOC AQUI
#GET FILE >> ADICIONAR DIRETORIO
def saveFilePatient(id, etype, FILES): #CRIA O DIRETÓRIO DOS DOCUMENTOS
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

    return True


#GER FILE >> retornar HTML
def fetchFilePatient(id):
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
def SaveEditionsPatientFunction(request):
    id_user = request.POST.get('id_user')
    type_doc = request.POST.get('type_doc')
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    saveFilePatient(id_user, type_doc, request.FILES)
    return {
        "response": True,
        "message": "Dados atualizados com sucesso."
    }


#CONTAGEM LEADS > TODOS LEADS
def CountLeadsFunction(request):
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nomeUser, unity in dados:
                pass

        param=(unity,)
        query = "SELECT COUNT(id_lead) AS qtd_geral FROM customer_refer.leads WHERE register = '0' AND unity_l = %s AND register = 0;"
        cursor.execute(query, param)
        
        dados = cursor
        array = []
        for qtd_geral in dados:
            newinfoa = ({
                "qtd_geral": qtd_geral[0]
                })
            array.append(newinfoa)
    return array


#CONTAGEM LEADS > MES
def CountLeadsMesFunction(request):
    dt_now = checkDayMonth("this_month")#aqui filtro mes
    dt_start = dt_now["dt_start"]
    dt_end = dt_now["dt_end"]
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nomeUser, unity in dados:
                pass

        param=(dt_start, dt_end,unity,)
        query = "SELECT COUNT(id_lead) AS qtd_mes FROM customer_refer.leads WHERE data_regis_l BETWEEN %s AND %s AND register = '0' AND unity_l = %s AND register = 0; "
        cursor.execute(query, param)
        dados = cursor
        array = []
        for qtd_mes in dados:
            newinfoa = ({
                "qtd_mes": qtd_mes[0]
                })
            array.append(newinfoa)
    return array

#CONTAGEM LEADS > DIA
def CountLeadsDayFunction(request):
    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nomeUser, unity in dados:
                pass

        param=(unity,)
        query = "SELECT COUNT(data_regis_l) AS qtd_dia FROM customer_refer.leads WHERE DATE(data_regis_l) = CURDATE() AND unity_l = %s AND register = 0;"
        cursor.execute(query, param)

        dados = cursor
        array = []
        for qtd_day in dados:
            newinfoa = ({
                "qtd_day": qtd_day[0]
                })
        array.append(newinfoa)
    return array

#CONTAGEM AGENDAMENTOS > CONCLUIDOS
def CountAgendamentsCSFunction(request):
    with connections['customer_refer'].cursor() as cursor:
        query = "SELECT COUNT(status) AS qtd_concl FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURDATE() AND status = 'Concluído';"
        cursor.execute(query)
        dados = cursor
        array = []

        for qtd_concl in dados:
            newinfoa = ({
                "qtd_concl": qtd_concl[0]
                })
            array.append(newinfoa)
    return array

#CONTAGEM AGENDAMENTOS > Frustrados
def CountAgendamentsFFunction(request):
    with connections['customer_refer'].cursor() as cursor:
        query = "SELECT COUNT(status) AS qtd_frust FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURDATE() AND status = 'Frustrado';"
        cursor.execute(query)
        dados = cursor
        array = []

        for qtd_frust in dados:
            newinfoa = ({
                "qtd_frust": qtd_frust[0]
                })
            array.append(newinfoa)
    return array

#CONTAGEM AGENDAMENTOS > CANCELADOS
def CountAgendamentsCFunction(request):
    with connections['customer_refer'].cursor() as cursor:
        query = "SELECT COUNT(status) AS qtd_canc FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURDATE() AND status = 'Cancelado';"
        cursor.execute(query)
        dados = cursor
        array = []

        for qtd_canc in dados:
            newinfoa = ({
                "qtd_canc": qtd_canc[0]
                })
            array.append(newinfoa)
    return array


#CONTAGEM AGENDAMENTOS > ATRASADOS  
def CountAgendamentAtrasadosFunction(request):
    date_create = str(datetime.now().strftime("%Y-%m-%d"))
    with connections['customer_refer'].cursor() as cursor:
        query = "SELECT COUNT(id)  FROM auth_agenda.collection_schedule WHERE status = 'Pendente' AND data_agendamento < %s"
        cursor.execute(query, (date_create,))
        dados = cursor
        array = []

        for qtd_atr in dados:
            newinfoa = ({
                "qtd_atr": qtd_atr[0]
                })
            array.append(newinfoa)
    return array


    
    #CONTAGEM AGENDAMENTOS > PENDENTES
def CountAgendamentsPFunction(request):
    with connections['customer_refer'].cursor() as cursor:
        query = "SELECT COUNT(id)  FROM auth_agenda.collection_schedule WHERE DATE(data_agendamento) = CURDATE() AND status = 'Pendente'"
        cursor.execute(query)
        dados = cursor
        array = []

        for qtd_geral in dados:
            newinfoa = ({
                "qtd_geral": qtd_geral[0]
                })
            array.append(newinfoa)
    return array


#TABELA USUARIOS
def searchUsersUnitSelect(request):
    Stp_perfil = request.POST.get("Stp_perfil")
    with connections['auth_users'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nomeUser, unity in dados:
                pass
        if Stp_perfil not in ["", None]:
            param =(Stp_perfil, unity,)
            query = "SELECT a.id, a.nome, b.descriptions,  a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.descriptions NOT LIKE 'parceiro' AND b.id =  %s AND a.unity = %s;"
            cursor.execute(query, param)
            dados = cursor.fetchall()
            array = []

            for id, nome, descriptions, status, unity in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "descriptions": descriptions,
                    "status": status,
                    "unity": unity,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                    })
                array.append(newinfoa)
            
            return {
                "message": array
            }
        else: 
            query = "SELECT a.id, a.nome, b.descriptions,  a.status, us.unit_s FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id INNER JOIN admins.units_shiloh us ON a.unity = us.id_unit_s WHERE b.descriptions NOT LIKE 'parceiro' AND a.unity = %s;"
            cursor.execute(query)
            dados = cursor.fetchall()
            array2 = []
        for id, nome, descriptions, status, unity in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "descriptions": descriptions,
                "status": status,
                "unity": unity,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                })
            array2.append(newinfoa)
                
        return {
            "message": array2
        }

#AGENDAR COLETA INTERNA - SELECT 2
def SearchSelectInterno(request):
    with connections['customer_refer'].cursor() as cursor:
        query= "SELECT a.id, a.nome, a.cpf, b.descriptions, a.tel1, c.unit_s FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON b.id = a.perfil INNER JOIN admins.units_shiloh c ON  c.id_unit_s = a.unity WHERE perfil NOT LIKE 7 ;"
        cursor.execute(query)
        dados = cursor
        array = []
        for id, nome, cpf, perfil, tel1, unity in dados:
            newinfoa = ({
                "id_p": id,
                "nome": nome,
                "cpf": cpf,
                "perfil": perfil,
                "tel1": tel1,
                "unity": unity,
                })
            array.append(newinfoa)
        return array

#API AGENDAR COLETA INTERNA
def FschedulePickupInt(request):
    date_age = request.POST.get("date_age")
    hr_age = request.POST.get("hr_age")
    tp_service = request.POST.get("tp_service")
    tp_exame = request.POST.get("tp_exame")
    convenio = request.POST.get("convenio")
    nurse = request.POST.get("nurse")
    name = request.POST.get("name")
    tel1 = request.POST.get("tel1") 
    obs = request.POST.get("obs")
    perfil = request.POST.get("perfil")
    unity = request.POST.get("unity")
    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    with connections['auth_agenda'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_usuario, nomeUser, unityU in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        params = (name, tel1, date_age, hr_age, tp_service, tp_exame, convenio, nurse, nomeUser, obs, date_create, unityU, perfil,)
        query = "INSERT INTO `auth_agenda`.`collection_schedule` (`id`, `nome_p`, `tel1_p`, `tel2_p`, `data_agendamento`, `hr_agendamento`, `tp_servico`, `tp_exame`, `convenio`, `resp_enfermeiro`, `motorista`, `resp_medico`, `resp_comercial`, `resp_atendimento`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `cidade`, `uf`, `val_cust`, `val_work_lab`, `val_pag`, `obs`, `status`, `motivo_status`, `resp_fin`, `data_fin`, `data_resgistro`, `unity`, `identification`, `perfil_int`) VALUES (NULL, %s, %s, '', %s, %s, %s, %s, %s, %s, '', '', '', %s, '', '', '', '', '', '', '', '', '', '', %s,'Pendente', '', '', '1969-12-31', %s, %s, 'Interno', %s);"
        cursor.execute(query, params)

    return {"response": "true", "message": "Agendado com sucesso!"}

#TABELA COLETA AGENDADA INTERNA
def searchScheduledPickupInt(request):
    
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

        Q = fetchQueryUnityFinance("unit.id_unit_s", perfil, unityY) 
        query = "SELECT unit.unit_s, a.id, pa.nome, a.tel1_p, a.data_agendamento, a.status, a.perfil_int FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users pa ON a.nome_p = pa.id INNER JOIN auth_users.users usrr ON usrr.nome = a.resp_atendimento INNER JOIN admins.units_shiloh unit ON unit.id_unit_s = usrr.unity WHERE  {} AND  a.identification LIKE 'Interno' AND a.status IN ('Pendente', 'Em Andamento') ORDER BY a.data_agendamento".format(Q)
        cursor.execute(query)
        dados = cursor.fetchall()
        array = []
        for  a_unity_int, a_id, us_nome, a_tel1_int, a_data_agendamento_int, a_status_int, a_perfil_int,  in dados:
            dataFormatada = datetime.strptime(str(a_data_agendamento_int), "%Y-%m-%d").strftime("%d/%m/%Y") if a_data_agendamento_int not in ["", None] else ""
            newinfoa = ({
                "id": a_id,
                "nome": us_nome,
                "perfil": a_perfil_int,
                "tel": a_tel1_int,
                "data_age": dataFormatada,
                "unity": a_unity_int,
                "status": a_status_int,
                })
            array.append(newinfoa)
    return array 

#MODAL COLETA AGENDADA INTERNA
def SearchModalScheduledInt(request):
    id = request.POST.get('id_user')

    with connections['customer_refer'].cursor() as cursor:
        params = (
            id,
        )
        query = "SELECT a.id, a.data_agendamento, a.hr_agendamento, b.tipo_servico, c.tipo_exame, g.nome_conv, e.nome, np.nome, a.tel1_p, a.obs, b.tipo_servico, c.tipo_exame, a.status, a.motivo_status, co.color, uni.unit_s , a.perfil_int FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN admins.health_insurance g ON a.convenio = g.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN admins.status_colors co ON a.status = co.status_c INNER JOIN auth_users.users np ON a.nome_p = np.id INNER JOIN admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE a.id = %s "
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for a_id, a_data_agendamento_int, a_hr_agendamento_int, b_tipo_servico, c_tipo_exame, g_nome_conv, e_nome, np_nome, a_tel1_int, a_obs_int, b_tipo_servico, c_tipo_exame, a_status_int, a_motivo_status_int, co_color, a_unity_int, a_perfil_int in dados:
                dict_response = {
                    "agendamento": {
                        "data_agendamento": a_data_agendamento_int,
                        "hr_agendamento": a_hr_agendamento_int,
                        "tipo_servico": b_tipo_servico,
                        "tipo_exame": c_tipo_exame,
                        "nurse": e_nome,
                        "convenio": g_nome_conv,
                        "id": a_id,
                        
                    },
                    "pessoal": {
                        "phone1": a_tel1_int,
                        "paciente": np_nome,
                    },
                    "obs": {
                        "obs": a_obs_int,
                        "statusM": a_status_int,
                        "motivo_status": a_motivo_status_int,
                        "color": co_color,
                        "unidade": a_unity_int,
                        "perfil": a_perfil_int,
                    },
                }
    
        query = "SELECT data_inc_proc_f, status_exame_f, resp_inicio_p_f, data_final_f FROM auth_finances.completed_exams WHERE id_agendamento_f = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        arrays=[]
        if dados:
            for data_inc_proc_f, status_exame_f,  resp_inicio_p_f, data_final_f in dados:
                array = {
                    "status": str(status_exame_f) if status_exame_f else "",
                    "date_proccess": {
                    "start": data_inc_proc_f if data_inc_proc_f else "0000-00-00",
                    "end": data_final_f if data_final_f else "0000-00-00",
                        
                    }
                }
                arrays.append(array)
        
    return {
        "response": False if not dict_response else True,
        "message": dict_response,
        "messages": arrays
    }

#ATUALIZAR STATUS DO AGENDAMENTO CONCLUIDO - INTERNO
def FunctionStatusAgendaConcInt(request):
    id = request.POST.get("id")
    data_atual = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
   
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
                "message": "Login expirado, faça login novamente para continuar."
            }

        param= (id_usuario, data_atual, id,)
        param2= ( id, data_atual,)
        query = "UPDATE `auth_agenda`.`collection_schedule` SET `status` = 'Concluído', `resp_fin` = %s, data_fin = %s WHERE (`id` = %s);"
        cursor.execute(query, param)

        query2 = "INSERT INTO `auth_finances`.`completed_exams` (`id`, `id_agendamento_f`, `status_exame_f`, `data_registro_f`, `regis`, `identification`) VALUES (NULL, %s, '8', %s, '0', 'Interno');"
        cursor.execute(query2, param2)
        
    return {"response": "true", "message": "Ok"}


#SELECT POR MES > COLETA INTERNA
def SearchMonthIntFunction(request):
    month = request.POST.get('month')
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

        Q = fetchQueryUnityFinance("unit.id_unit_s", perfil, unityY) 
        query = "SELECT unit.unit_s, a.id, pa.nome_p, a.tel1_p, a.data_agendamento, a.status, a.perfil_int FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_users.users usrr ON usrr.nome = a.resp_atendimento INNER JOIN admins.units_shiloh unit ON unit.id_unit_s = usrr.unity WHERE  {} AND a.identification LIKE 'Interno' ORDER BY a.data_agendamento AND DATE_FORMAT( a.data_agendamento, '%m') = %s".format(Q)
        cursor.execute(query, (month,))
        dados = cursor
        array = []
        for  a_unity_int, a_id, us_nome, a_tel1_int, a_data_agendamento_int, a_status_int, a_perfil_int,  in dados:
            dataFormatada = datetime.strptime(str(a_data_agendamento_int), "%Y-%m-%d").strftime("%d/%m/%Y") if a_data_agendamento_int not in ["", None] else ""
            newinfoa = ({
                "id": a_id,
                "nome": us_nome,
                "perfil": a_perfil_int,
                "tel": a_tel1_int,
                "data_age": dataFormatada,
                "unity": a_unity_int,
                "status": a_status_int,
                })
            array.append(newinfoa)
    return array 




#TABELA COLETA CONCLUIDA - INTERNA
def RetfundFConcl(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome, a.data_agendamento, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users pa ON a.nome_p = pa.id INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND sp.regis LIKE  '0' AND a.identification LIKE 'Interno' ORDER BY data_agendamento ASC;"
        cursor.execute(query)
        dados = cursor
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



#TABELA COLETA CONCLUIDA - INTERNA
def RetfundFFinalizado(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN auth_users.users pa ON a.nome_p = pa.id INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE  a.status = 'Concluído' AND sp.regis LIKE  '1' AND a.identification LIKE  'Interno'"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, paciente, dataconc, datainicio, datafim, status, status_p in dados:
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "dataconc": convertDate(dataconc),
                "datainicio": convertDate(datainicio),
                "datafim": convertDate(datafim),
                "status": status,
                "status_p": status_p,
                })
            array.append(newinfoa)
    return array



#TABELA ROTA DAS ENFERMEIRAS
def searchRouteNurse(request):
    hoje = (datetime.today().strftime('%Y-%m-%d'))
    amanha = date.today() + timedelta(days=1)


    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT a.perfil, a.id, a.nome, a.unity FROM auth_users.users a INNER JOIN admins.units_shiloh b ON a.unity = b.id_unit_s WHERE login LIKE %s"
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

        querydate = "SELECT CURDATE(), DATE_ADD(CURDATE(), INTERVAL 1 DAY)"
        cursor.execute(querydate)
        dados = cursor.fetchall()
        if dados:
            for hoje, amanha in dados: 
                pass

        query = "SELECT unit.unit_s, a.id, pa.nome_p, a.tel1_p, b.tipo_servico, c.tipo_exame, a.resp_medico, a.data_agendamento, a.status, a.hr_agendamento FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_users.users usrr ON usrr.nome = a.resp_atendimento INNER JOIN admins.units_shiloh unit ON unit.id_unit_s = usrr.unity WHERE a.resp_enfermeiro = %s AND a.status IN ('Pendente', 'Em Andamento') AND a.identification LIKE  'Externo' AND a.data_agendamento IN (%s, %s) ORDER BY a.data_agendamento, a.data_agendamento ASC"
        params = (id_usuario, hoje, amanha)
        cursor.execute(query, params)
        dados = cursor.fetchall()
        array = []

        for unity, id, paciente, phone, service, exame, doctor, data, status, hr_age  in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "id": id,
                "unity": unity,
                "paciente": paciente,
                "phone": phone,
                "service": service,
                "exame": exame,
                "hr_age": hr_age,
                "date_age": dataFormatada,
                "status": status,
                })
            array.append(newinfoa)
    return array 




#COLETA EM ANDAMENTO
def IniciarColetaFunction(request):
    id = request.POST.get("id")
    with connections['auth_users'].cursor() as cursor:
        query = "UPDATE auth_agenda.collection_schedule SET status = 'Em Andamento' WHERE id = %s;"
        cursor.execute(query, (id,))

    return {"response": "true", "message": "Ok"}





def iInfoLog(request):
    with connections['admins'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()

        if dados:
            for id, nomeLog, unity in dados:
                dict_response = {
                    "teste": {
                        "id": id,
                        "nomeLog": nomeLog,
                        "unity": unity,
                    },
                }   
            return {
                "response": False if not dict_response else True,
                "message": dict_response
            }



#CADASTRAR PARCEIROS
def StatusNegative(request):
    checkbox = request.POST.get("checkbox")
    id_lead = request.POST.get("id_lead")
    with connections['auth_users'].cursor() as cursor:
        query = "UPDATE `customer_refer`.`leads` SET `status_l` = %s WHERE (`id_lead` = %s);"
        cursor.execute(query, (checkbox, id_lead,))

    return {"response": "true", "message": "Atualizado com sucesso!"}



def FunctionSearchStatusLead(request):
    with connections['admins'].cursor() as cursor:
        query = "SELECT id, status FROM admins.stataus_lead;"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, status in dados:
            newinfoa = ({
                "id": id,
                "status": status,
                })
            array.append(newinfoa)

        return array

#FILTRO DE STATUS LEADS
def SearchStatusLeadFilterFunction(request):
    statusL = request.POST.get("statusL")

    with connections['customer_refer'].cursor() as cursor:
        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dadosU = cursor.fetchall()
        if dadosU:
            for id_usuarioU, nomeU, unity in dadosU:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
        query= "SELECT a.id_lead, a.nome_lead, a.tel1_lead, a.data_regis_l, b.nome, a.unity_l, status_l FROM customer_refer.leads a INNER JOIN auth_users.users b ON a.medico_resp_l = b.id  WHERE a.unity_l = %s AND status_l = %s ORDER BY a.data_regis_l desc"
        cursor.execute(query, (unity, statusL,))
        dados = cursor
        array = []
        for id, nome, telefone, data, medico_resp, unity, status in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "id": id,
                "nome": nome,
                "telefone": telefone,
                "data": dataFormatada,
                "medico_resp": medico_resp,
                "nomeU": nomeU,
                "status": status,
                })
            array.append(newinfoa)
    return {
        "response": True,
        "message": array
    }

#------------------------------------------- DOCS FINANCEIROS --------------------------------------------


#SERVE PARA CRIAR O DIRETÓRIO DO MEU ARQUIVO
def ApiGerFilePartnersFunction(id, month, FILES):

    PATH = settings.BASE_DIR_DOCS + "/partners/finances/{}"  # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    PATH_USER = PATH.format(id) # ADICIONANDO ID NO {} DE CIMA /\
    PATH_TYPES = PATH_USER + "/" + "NF" + "/" + month + "/" # AQUI ESTÁ INDO PARA O DIRETORIO: docs/patients/process/ID/tipo_do_arquivo
    
    arr_dir = []
    for name, file in FILES.items():
        file_name = default_storage.save(PATH_TYPES + file.name, file)
        arr_dir.append({
            "name": file.name,
            "path": PATH_TYPES + file.name
        })
    return True


#QUANDO CLICAR NO BOTÃO, EXECUTA ESSA FUNÇÃO.
def ApiNfPartnersFunction(request):
    id_partners = request.POST.get('id_partners')
    month = request.POST.get('month')
    if (month == ""):
        month = str(datetime.now().strftime("%m-%Y"))
    else:
        month = (month + str(datetime.now().strftime("-%Y")))

    date_create = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #chama função externa
    ApiGerFilePartnersFunction(id_partners, month, request.FILES)
    return {
        "response": True,
        "message": "Dados atualizados com sucesso."
    }



def FetchPartnersFilesFunction(bodyData): #to aqui
    try:
        keysLIST = []
        month = bodyData.month
        if (month == ""):
            month = (month) = str(datetime.now().strftime("0%m-%Y"))
        else:
            month = (month + str(datetime.now().strftime("-%Y")))
        
        id = bodyData.id_user
        PATH = settings.BASE_DIR_DOCS + f"/partners/finances/{id}/NF/" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
        PATH_ORIGIN = f"/partners/finances/{id}/NF"
        DS = default_storage
        if DS.exists(PATH):
            LIST_TYPES = DS.listdir(PATH)
            if LIST_TYPES:
                if len(LIST_TYPES) > 0:
                    arrLIST = []
                    for key in LIST_TYPES[0]:
                        arrLIST.append(key)
                    if arrLIST:
                        for paths in arrLIST:
                            arrLISTPATHS = DS.listdir(f"{PATH}/{paths}")
                            for key in arrLISTPATHS[1]:
                                keysLIST.append({
                                    "type": str(paths),
                                    "type_desc": settings.LISTPATHTYPEFINANCE.get(str(paths), ""),
                                    "name": key,
                                    "path": PATH_ORIGIN + f"/{paths}/{key}",
                                    "date_create": {
                                        "en": str(default_storage.get_created_time(f"{PATH}/{paths}/{key}").date()),
                                        "pt": str(default_storage.get_created_time(f"{PATH}/{paths}/{key}").strftime("%d/%m/%Y"))
                                    },
                                    "url": settings.SHORT_PLATAFORM + f"/docs/partners/finances/{id}/{paths}/{key}"
                                })
        return {
            "response": True,
            "message": {
                "docs": keysLIST,
            }
        }

    except Exception as err:
        print("EROOOOO>>", err)
        return {
            "response": False,
            "message": "Não foi possível encontrar este parceiro."
        }






#GET FILE REMOVE
def RemoveFilePartnersFunction(request):
    id_partners = request.POST.get('id_partners')
    type_file = request.POST.get('type_file')
    name_file = request.POST.get('name_file')

    try:
        id_partners = int(id_partners)
    except:
        return {
            "response": "false",
            "message": "Não foi possível encontrar este arquivo."
        }
    
    PATH = settings.BASE_DIR_DOCS + f"/partners/finances/{id_partners}/NF/{type_file}/{name_file}" # PATH ORIGINAL, {} SERVE PARA VOCÊ ADICIONAR O "ID" NO DIRETORIO
    if default_storage.exists(PATH):
        try:
            default_storage.delete(PATH)
            if not default_storage.exists(PATH):
                return {
                    "response": "true",
                    "message": "Arquivo excluido com sucesso."
                }
        except:
            pass
    else:
        return {
            "response": "true",
            "message": "Arquivo excluido com sucesso."
        }
    
    return {
        "response": "false",
        "message": "Não foi possível encontrar ou remover este arquivo."
    } 



#PRÉ CADASTRO PARCEIROS
def CadastrePrePartners(request):
    categoria = request.POST.get("categoria")
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
    padrao = request.POST.get("padrao")
    porcentagem = request.POST.get("porcentagem")
    fixo = request.POST.get("fixo")

    padraos = padrao.replace(",", ".").replace("R$", "")
    porcentagems = porcentagem.replace("%", "")
    fixos = fixo.replace(".", "|").replace(",", ".").replace("|", "")

    padraoC = float (padraos) if padraos not in ["", None] else None
    porcentagemC = float (porcentagems) if porcentagems not in ["", None] else None
    fixoC = float (fixos) if fixos not in ["", None] else None


    with connections['auth_users'].cursor() as cursor:
        qVerif =  "select id, nome, tel1 FROM auth_users.users WHERE nome LIKE %s AND tel1 LIKE %s"
        cursor.execute(qVerif, (name, tel1,))
        dados = cursor.fetchall()
        
        if dados:
            return {"response": "true", "message": "Parceiro já cadastrado."}
        
        else:
            param =(name, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, rn, obs, categoria, padraoC, porcentagemC, fixoC,)
            query = "INSERT INTO `auth_users`.`users` (`id`, `perfil`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`, `status`, `resp_comerce`, `data_regis`, `unity`, `val_padrao`, `val_porcentagem`, `val_fixo`) VALUES (NULL, '7', '', %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '', 'Pré-Cadastro', '3', NULL, '1', %s, %s, %s);"
            cursor.execute(query, param,)
        
        return {"response": "true", "message": "Pré-cadastrado com sucesso!"}



#PRÉ CADASTRO PARCEIROS
def CadastrePrePartnersFunctionBNT(request):
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
    id_partners = request.POST.get("id_user")
    categoria = request.POST.get("categoria")
    year = str(datetime.now().strftime("%d%Y"))
    data_atual = str(datetime.now().strftime('%Y-%m-%d'))
    padrao = request.POST.get("padrao")
    porcentagem = request.POST.get("porcentagem")
    fixo = request.POST.get("fixo")

    with connections['auth_users'].cursor() as cursor:

        padraos = padrao.replace(",", ".").replace("R$", "")
        porcentagems = porcentagem.replace("%", "")
        fixos = fixo.replace(".", "|").replace(",", ".").replace("|", "")

        padraoC = float (padraos) if padraos not in ["", None] else None
        porcentagemC = float (porcentagems) if porcentagems not in ["", None] else None
        fixoC = float (fixos) if fixos not in ["", None] else None

        searchID = "SELECT id, nome, unity FROM auth_users.users WHERE login LIKE %s"
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for id_comercial, nome, unity in dados:
                pass
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }

        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")

        param =(name, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, rn, obs, categoria, rn,  id_comercial , data_atual, unity, padraoC, porcentagemC, fixoC, id_partners,)

        query = "UPDATE `auth_users`.`users` SET `nome` = %s, `email` = %s, `tel1` = %s, `tel2` = %s, `cep` =  %s, `rua` = %s, `numero` = %s, `complemento` = %s, `bairro` = %s, `city` = %s, `uf` = %s, `rn` = %s, `obs` = %s, `categoria` = %s, `login` = %s, `status` = 'Ativo', `resp_comerce` = %s, `data_regis` = %s, `unity` = %s, `val_padrao` = %s, `val_porcentagem` = %s, `val_fixo` = %s  WHERE (`id` = %s);"
        cursor.execute(query, param)

        if User.objects.filter(username=rn).exists():
            user = User.objects.get(username=rn)
            user.nome = rn
            user.email = email

            user.save()
        else:
           user = User.objects.create_user(username=rn, email=email, first_name=name, last_name='', password=year)
        
        #PERMISSÕES PRÉ DEFINIDAS ASSIM QUE CADASTRADAS
        arrayPermission = {
           "7":  ["20", "16",], #PARCEIRO(RETIRAR ALGUMAS PERMISSOES)
        }
        try:
            dictP = arrayPermission[str("7")]
        except:
            dictP = []
        
        if dictP:
            for id_permission in dictP:
                params = (
                    id_permission,
                    id_comercial,
                )
                query = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id_permission`, `id_user`, `nome_user`) VALUES (%s, %s, '')"
                cursor.execute(query, params)

            return {"response": "true", "message": "Cadastrado com sucesso!"}



    #PRÉ CADASTRO PARCEIROS
def PrePartnerCancelFunction(request):
    id_partners = request.POST.get("id_user")

    with connections['auth_users'].cursor() as cursor:

        query = "UPDATE `auth_users`.`users` SET `status` = 'Cancelado'  WHERE (`id` = %s);"
        cursor.execute(query, (id_partners,))

    return {"response": "true", "message": "Pré-cadastro cancelado."}



#SELECT COM TODOS OS COMERIAIS ATIVOS
def searchComercialFunction(request):
    with connections['userdb'].cursor() as cursor:
        query = "SELECT id, nome, status FROM auth_users.users where perfil = 6 AND status = 'Ativo';"
        cursor.execute(query)
        dados = cursor
        array = []
        for id, nome, status in dados:
            newinfoa = ({
                "id": id,
                "status": status,
                "nome": nome
                })
            array.append(newinfoa)
        return array


#MEUS PARCEIROS
def ApiAttPartnersFunction(request):
    if not allowPermission(request, "meus_registros_parceiros"):
        return json_without_success("Você não possui permissão para fazer esse tipo de alteração.")

    else:
        
        bodyData = request.POST #var para não precisar fazer tudo um por um
        print("passei aquii")

        id_user = bodyData.get('id_user')
        perfil = bodyData.get('perfil')
        padrao = bodyData.get('padrao').replace(",", ".").replace("R$", "")
        porcentagem = bodyData.get('porcentagem').replace("%", "")
        fixo = bodyData.get('fixo').replace(".", "|").replace(",", ".").replace("|", "").replace("R$", "")

        resp_commerce = bodyData.get('resp_commerce')

        padrao = float(padrao) if padrao not in ["", None] else None
        porcentagem = float(porcentagem) if porcentagem not in ["", None] else None
        fixo = float(fixo) if fixo not in ["", None] else None

        dataKeys = { #DICT PARA PEGAR TODOS OS VALORES DO AJAX
            #key, value >> valor que vem do ajax, valor para onde vai (banco de dados)
            "cpf": "cpf",
            "name": "nome",
            "date_nasc": "data_nasc",
            "email": "email",
            "tel1": "tel1",
            "tel2": "tel2",
            "zipcode": "cep",
            "addres": "rua",
            "number": "numero",
            "complement": "complemento",
            "district": "bairro",
            "city": "city",
            "uf": "uf",
            "rn": "rn",
            "categoria": "categoria",
            "obs": "obs",  
            "unity": "unity",  
        }
        print(dataKeys)
        
        db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
        cursor = db.connection()
        
        if resp_commerce == "" or resp_commerce == None:
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

            resp_commerce = id_usuario
        else:
            pass

        for key in dataKeys:
            try:
                query = "SELECT id, nome, status FROM auth_users.users where nome LIKE %s"
                cursor.execute(query, (resp_commerce,))
                dados = cursor.fetchall()
                for idC, nomeC, statusC in dados:
                    print(dados)
                    if idC != "":
                        resp_commerce = idC
                        print("1>>>>", resp_commerce)
                    
                if key in bodyData:#SE MEU VALOR DO INPUT DO AJAX EXISTIR DENTRO DO MEU POST, FAZ A QUERY
                    query = "UPDATE auth_users.users SET {} = %s, resp_comerce = %s, val_padrao = %s, val_porcentagem = %s, val_fixo = %s WHERE id = %s ".format(dataKeys[key]) #format serve para aplicar o método de formatação onde possui o valor da minha var dict e colocar dentro da minha chave, para ficar no padrão de UPDATE banco
                    params = (
                        bodyData.get(key), #serve para complementar o POST e obter o valor do input
                        resp_commerce,
                        padrao,
                        porcentagem,
                        fixo,
                        id_user,
                    )
                    cursor.execute(query, params)
            except:
                print("ERRROOO")
                query = "SELECT id FROM auth_permissions.permissions_type WHERE descriptions = %s"
                params = (
                    perfil,
                )    
                cursor.execute(query, params)
                dados = cursor.fetchall()
                for id in dados:
                    pass

                    if key in bodyData:
                        query = "UPDATE auth_users.users SET {} = %s, perfil = %s WHERE id = %s ".format(dataKeys[key])
                        params = (
                            bodyData.get(key),
                            id,
                            id_user,
                        )
                        print(params)
                        cursor.execute(query)
        return {
            "response": True,
            "message": "Dados atualizados com sucesso."
        }