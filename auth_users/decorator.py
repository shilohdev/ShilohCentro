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
from functions.connection.models import Connection
from functions.general.decorator import convertDate, checkDayMonth
from auth_finances.functions.exams.models import FinancesExams



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
    id_user = request.POST.get("id_user")
    
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
            param2 = (tp_perfil, cpf, name, date_nasc, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, id_user,)
            query2 = "UPDATE users SET perfil = %s, cpf = %s, nome = %s, data_nasc = %s, email = %s, tel1 = %s, tel2 = %s, cep = %s, rua = %s, numero = %s, complemento = %s, bairro = %s, city = %s, uf = %s WHERE id = %s"
            cursor.execute(query2, param2)
        else:
            param = (tp_perfil, cpf, name, date_nasc, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, cpf, )
            query = "INSERT INTO `auth_users`.`users` (`id`, `perfil`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`, `status`, `resp_comerce`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '', '', %s, '', 'Ativo', '');"
            cursor.execute(query, param)
            id_user = cursor.lastrowid

        #AUTENTICAÇÃO E CRIAÇÃO DE LOGIN E SENHA    
        if User.objects.filter(username=cpf).exists():
            user = User.objects.get(username=cpf)
            user.nome = name
            user.email = email

            user.save()
        else:
           user = User.objects.create_user(username=cpf, email=email, first_name=name, last_name='', password=cpf)
        
        #PERMISSÕES PRÉ DEFINIDAS ASSIM QUE CADASTRADAS
        arrayPermission = {
            "1": ["3", "4","1", "2", "8", "9", "10", "11", "12", "14", "15","16","17"],  #ADMINISTRADOR
            "2": ["3", "4", "2", "8", "9", "10", "11", "12", "14","15","16","17"], #ATENDIMENTO (RETIRAR ALGUMAS PERMISSOES)
            "3": ["3", "4","1", "2", "8", "9", "10", "11", "12", "14","15","16","17"], #ENFERMAGEM
            "5": ["3", "4","1", "2", "8", "9", "10", "11", "12", "14","15","16","17"], #FINANCEIRO
            "6": ["3", "4","1", "2", "8", "9", "10", "11", "12", "14","15","16","17"], #COMERCIAL
            "7": ["3", "4", "2", "8", "9", "10", "12", "14","15","16", "17"], #PARCEIRO(RETIRAR ALGUMAS PERMISSOES)
            "8": ["3", "4","1", "2", "8", "9", "10", "11", "12", "14","15","16","17"], #MOTORISTA
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
    year = str(datetime.now().strftime("%Y"))
    print(categoria)
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

        #CADASTRAR PERFIL
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)
        zipcode = zipcode.replace("-", "")

        param =(name, email, tel1, tel2, zipcode, addres, number, complement, district, city, uf, rn, obs, categoria, rn,id_usuario,)
        query = "INSERT INTO `auth_users`.`users` ( `id`, `perfil`, `cpf`, `nome`, `data_nasc`, `email`, `tel1`, `tel2`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `city`, `uf`, `rn`, `obs`, `categoria`, `login`, `senha`, `status`, `resp_comerce`) VALUES (NULL, '7', '', %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', 'Ativo', %s);"
        cursor.execute(query, param)
        id_user = cursor.lastrowid

#TESTE PARA SABER SE CONSIGO CORRIGIR AS PERMISSOES MEDICO 2
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
           "7": ["3", "4", "2", "8", "9", "10", "12", "14","15","16", "17"], #PARCEIRO(RETIRAR ALGUMAS PERMISSOES)
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


#CADASTRAR LEAD / INDICAÇÃO
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
   

    
    with connections['customer_refer'].cursor() as cursor:
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
        cpf = formatcpfcnpj(cpf)
        tel1 = formatTEL(tel1)
        tel2 = formatTEL(tel2)

        param =(cpf, name, email, tel1, tel2, convenio, checkbox, obs, id_usuario, data_atual,)
        query = "INSERT INTO `customer_refer`.`leads` (`id_lead`, `cpf_lead`, `nome_lead`, `email_lead`, `tel1_lead`, `tel2_lead`, `convenio_lead`, `tp_exame`, `obs_l`, `medico_resp_l`, `register`, `data_regis_l` ) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s);"
        cursor.execute(query, param)
        #PEGAR O ID DO USUARIO PARA INSERIR NA TABELA, ID ESTÁ VINDO VAZIO
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
        query = "SELECT id, perfil, nome FROM auth_users.users where perfil = 3;"
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
        query = "SELECT id, perfil, nome FROM auth_users.users where perfil = 8;"
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
        query = "SELECT id, nome_conv, status FROM admins.health_insurance;"
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
        query = "SELECT * FROM admins.exam_type;"
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
    attendance = request.POST.get("attendance") #aqui parceiro
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
        params = (name, tel1, tel2, date_age, hr_age, tp_service, tp_exame, convenio, nurse, driver, doctor, attendance, commerce, zipcode, addres, number,complement, district, city, uf, val_cust, val_work_lab, val_pag, obs, date_create,)
        query = "INSERT INTO `auth_agenda`.`collection_schedule` (`id`, `nome_p`, `tel1_p`, `tel2_p`, `data_agendamento`, `hr_agendamento`, `tp_servico`, `tp_exame`, `convenio`, `resp_enfermeiro`, `motorista`, `resp_medico`, `resp_comercial`, `resp_atendimento`, `cep`, `rua`, `numero`, `complemento`, `bairro`, `cidade`, `uf`, `val_cust`, `val_work_lab`, `val_pag`, `obs`, `status`, `motivo_status`, `resp_fin`, `data_fin`, `data_resgistro`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'Pendente', '', '', '1969-12-31', %s);"
        cursor.execute(query, params)
    return {"response": "true", "message": "Agendado com sucesso!"}


def searchDoctor(request):
    with connections['userdb'].cursor() as cursor:
        query = "SELECT perfil, nome FROM auth_users.users where perfil = 7 ;"
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

    print(dictPost)

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

    # VARIABLES
    S_COLUMNS = ""
    S_TABLE = "auth_agenda.collection_schedule cs INNER JOIN customer_refer.patients au2 ON au2.id_p = cs.nome_p INNER JOIN auth_users.users au ON au.id = cs.resp_enfermeiro INNER JOIN admins.type_services ts ON ts.id = cs.tp_servico INNER JOIN admins.health_insurance hi ON hi.id = cs.convenio INNER JOIN admins.exam_type et ON et.id = cs.tp_exame"
    S_CONDITION = "WHERE "
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


    S_COLUMNS = "cs.id, au2.nome_p, cs.tel1_p, ts.tipo_servico, et.tipo_exame, au.nome as resp_enfermeiro, cs.resp_medico, cs.data_agendamento, cs.status"
    S_CONDITION = S_CONDITION[:-5]

    db = Connection('admins', '', '', '', '')

    db.table = S_TABLE
    db.params = tuple(params)
    db.condition = "{}".format(S_CONDITION)

    print(db.table)
    print(db.params)
    print(db.condition)

    arr_response = []

    try:
        dados = db.fetch([S_COLUMNS], True)
        if dados:
            for id, nome_p, tel1_p, tp_servico, tp_exame, resp_enfermeiro, resp_medico, data_agendamento, status in dados:
                arr_response.append({
                    "id": id,
                    "name": nome_p,
                    "tel": tel1_p, 
                    "servico": tp_servico, 
                    "exame": tp_exame,
                    "enfermeiro": resp_enfermeiro,  
                    "medico": resp_medico,
                    "agendamento": convertDate(data_agendamento),
                    "status": status
                })
    except Exception as err:
        db.condition = ""
        dados = db.fetch([S_COLUMNS], False)
        if dados:
            for id, nome_p, tel1_p, tp_servico, tp_exame, resp_enfermeiro, resp_medico, data_agendamento, status in dados:
                arr_response.append({
                    "id": id,
                    "name": nome_p,
                    "tel": tel1_p, 
                    "servico": tp_servico, 
                    "exame": tp_exame,
                    "enfermeiro": resp_enfermeiro,  
                    "medico": resp_medico,
                    "agendamento": convertDate(data_agendamento),
                    "status": status
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
        query = "SELECT a.id, a.nome, a.status, b.descriptions FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id WHERE descriptions NOT LIKE 'parceiro';"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, nome, status, descriptions in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "descriptions": descriptions,
                "status": status,
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
            query = "SELECT a.id, a.nome, b.descriptions, a.status FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id WHERE b.descriptions NOT LIKE 'parceiro' AND b.id =  %s;"
            cursor.execute(query, param)
            dados = cursor.fetchall()
            array = []
            for id, nome, descriptions, status in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "descriptions": descriptions,
                    "status": status,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                    })
                array.append(newinfoa)
            
            return {
                "message": array
            }
        else: 
            query = "SELECT a.id, a.nome, b.descriptions, a.status FROM auth_users.users a INNER JOIN auth_permissions.permissions_type b ON a.perfil = b.id WHERE descriptions NOT LIKE 'parceiro'"
            cursor.execute(query)
            dados = cursor.fetchall()
            array2 = []

        for id, nome, descriptions, status in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "descriptions": descriptions,
                "status": status,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                })
            array2.append(newinfoa)
                
        return {
            "message": array2
        }

#CHANGE STATUS > ativa e desativa
def ApiChangeStatusFunction(request):
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
    db.table = "auth_users.users u" #VAR COM CONEXAO TABLE
    db.condition = "WHERE u.id = %s" #VAR COM A CONDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM 
    dados = db.fetch(["u.perfil, u.cpf, u.nome, u.data_nasc, u.email, u.tel1, u.tel2, u.cep, u.rua, u.numero, u.complemento, u.bairro, u.city, u.uf"], True)
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for u_perfil, u_cpf, u_nome, u_data_nasc, u_email, u_tel1, u_tel2, u_cep, u_rua, u_numero, u_complemento, u_bairro, u_city, u_uf in dados:
            dict_response = { #VARIAVEL COM OS DICTS
                "id": id_user,
                "perfil": u_perfil,
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
            query = "SELECT  a.id, a.nome, b.categoria, a.status FROM auth_users.users a INNER JOIN auth_users.Category_pertners b ON a.categoria = b.id WHERE b.id LIKE %s"
            cursor.execute(query, param)
            dados = cursor.fetchall()
            array = []

            for id, nome, categoria, status in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "categoria": categoria,
                    "status": status,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"
                })
                array.append(newinfoa)
            
            return {
                "response": True,
                "message": array
            }
        else:
            query = "SELECT  a.id, a.nome, b.categoria, a.status FROM auth_users.users a INNER JOIN auth_users.Category_pertners b ON a.categoria = b.id WHERE b.id"
            cursor.execute(query)
            dados = cursor.fetchall()
            array2 = []

            for id, nome, categoria, status in dados:
                newinfoa = ({
                    "id": id,
                    "nome": nome,
                    "categoria": categoria,
                    "status": status,
                    "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"

                    })
                array2.append(newinfoa)
                    
            return {
                "response": True,
                "message": array2
            }

#SELECT TABELA PARCEIROS AQUI PARCEIRO
def TabelaPartners(request):
    with connections['auth_permissions'].cursor() as cursor:
        query = "SELECT  a.id, a.nome, c.categoria, a.rn, a.status, rc.nome FROM auth_users.users a INNER JOIN auth_users.Category_pertners c ON a.categoria = c.id INNER JOIN auth_users.users rc ON a.resp_comerce = rc.id"
        cursor.execute(query)
        dados = cursor
        array = []
            
        for id, nome, categoria, rn, status, resp_comercial in dados:
            newinfoa = ({
                "id": id,
                "nome": nome,
                "resp_comercial": resp_comercial,
                "categoria": categoria,
                "status": status,
                "rn": rn,
                "btn_status": "#76c076da" if status.upper() == "ATIVO" else "#c74d4d"

                })
            array.append(newinfoa)

        return array

#MODAL PARCEIROS
def ApiViewDataPartnersModalFunction(request):
    dict_response = {} #VARIAVEL VAZIA PARA RECEBER O DICT

    try:
        id_user = int(request.POST.get('id_user'))
    except:
        return {
            "response": False,
            "message": "Nenhum usuário encontrado com este id."
        }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    db.table = "auth_users.users p" #VAR COM CONEEXAO TAVLE
    db.condition = "WHERE p.id = %s" #VAR COM A CONDDIÇÃO UTILIZADA NO BANCO
    db.params = (id_user,) #VAR COM O PARAM
    dados = db.fetch(["p.nome, p.email, p.tel1, p.tel2, p.cep, p.rua, p.numero, p.complemento, p.bairro, p.city, p.uf, p.rn, p.obs, p.categoria"], True)
    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for p_nome, p_email, p_tel1, p_tel2, p_cep, p_rua, p_numero, p_complemento, p_bairro, p_city, p_uf, p_rn, p_obs, p_categoria in dados:
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
                }
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

#UPDATE PARCEIRO E USUARIO INTERNO
def ApiChangeUsersModalFunction(request):
    bodyData = request.POST #var para não precisar fazer tudo um por um

    id_user = bodyData.get('id_user')
    dataKeys = { #DICT PARA PEGAR TODOS OS VALORES DO AJAX
        "tp_perfil": "perfil", #key, value >> valor que vem do ajax, valor para onde vai (banco de dados)
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
        
    }

    db = Connection('userdb', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    cursor = db.connection()

    for key in dataKeys:
        if key in bodyData:#SE MEU VALOR DO INPUT DO AJAX EXISTIR DENTRO DO MEU POST, FAZ A QUERY
            query = "UPDATE auth_users.users SET {} = %s WHERE id = %s".format(dataKeys[key]) #format serve para aplicar o método de formatação onde possui o valor da minha var dict e colocar dentro da minha chave, para ficar no padrão de UPDATE banco
            params = (
                bodyData.get(key), #serve para complementar o POST e obter o valor do input
                id_user,
            )
            cursor.execute(query, params)

            print(query, params)

    return {
        "response": True,
        "message": "Dados atualizados com sucesso."
    }

    
#SELECT INDICAÇÃO/PACIENTES LISTAR
def searchIndication(request):
    with connections['customer_refer'].cursor() as cursor:
        params = (
            request.user.username,
        )

        query= "SELECT a.id_p, a.nome_p, b.nome  FROM customer_refer.patients a INNER JOIN auth_users.users b ON a.medico_resp_p = b.id" #cortei  WHERE b.login LIKE %s
        cursor.execute(query, )
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
    
    with connections['customer_refer'].cursor() as cursor:
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
        param = (lead, cpf, name, email, data_nasc, tel1, tel2, cep, rua, numero ,complement, bairro, cidade, uf, conv_medico, medico_resp, id_usuario,)
        query="INSERT INTO `customer_refer`.`patients` (`id_p`, `id_l_p`, `cpf_p`, `nome_p`, `email_p`, `data_nasc_p`, `tel1_p`, `tel2_p`, `cep_p`, `rua_p`, `numero_p`, `complemento_p`, `bairro_p`, `cidade_p`, `uf_p`, `convenio_p`, `medico_resp_p`, `atendente_resp_p`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, param)

        query2= "UPDATE `customer_refer`.`leads` SET `register` = '1' WHERE (`id_lead` = '1');"
        cursor.execute(query2)

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

#SELECT INDICAÇÃO/LEADS # aqui lid
def searchLead(request):
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
    dados = db.fetch(["a.id_p, a.id_l_p, a.cpf_p, a.nome_p, a.email_p, a.data_nasc_p, a.tel1_p, a.tel2_p, a.cep_p, a.rua_p, a.numero_p, a.complemento_p, a.bairro_p, a.cidade_p, a.uf_p, b.id, d.nome, e.nome"], True)

    if dados:#VARIAVEL DADOS COM TODOS OS PARAMETROS SOLICITADOS PARA OS USUARIOS
        for id_p, id_l_p, cpf_p, nome_p, email_p, data_nasc_p, tel1_p, tel2_p, cep_p, rua_p, numero_p, complemento_p, bairro_p, cidade_p, uf_p, id, nome_m, nome_a  in dados:
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

#AGENDAR COLETA SELECT2 LEADS
def SearchSelectSchedule(request):
    with connections['customer_refer'].cursor() as cursor:
        #query= "SELECT a.id_p, a.cpf_p, a.nome_p, a.tel1_p, a.tel2_p, a.cep_p, a.rua_p, a.numero_p, a.complemento_p, a.bairro_p, a.cidade_p, a.uf_p, c.nome, d.nome FROM customer_refer.patients a INNER JOIN auth_users.users d ON a.atendente_resp_p = d.id INNER JOIN auth_users.users c ON a.medico_resp_p = c.id"
        query= "SELECT a.id_p, a.cpf_p, a.nome_p, a.tel1_p, a.tel2_p, a.cep_p, a.rua_p, a.numero_p, a.complemento_p, a.bairro_p, a.cidade_p, a.uf_p, c.nome, d.nome, RES.nome FROM customer_refer.patients a INNER JOIN auth_users.users d ON a.atendente_resp_p = d.id INNER JOIN auth_users.users c ON a.medico_resp_p = c.id INNER JOIN auth_users.users RES ON  c.resp_comerce = RES.id;"
        cursor.execute(query)
        dados = cursor
        array = []
        for id, cpf, nomep, tel1, tel2, cep, rua, numero, complemento, bairro, cidade, uf, nome_med, nome_ate, nome_commerce  in dados:
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
                "nome_ate": nome_ate,
                "nome_commerce": nome_commerce,
                })
            array.append(newinfoa)
        return array #pega os valores


#TABELA COLETA AGENDADA
def searchScheduledPickup(request):
    dt_now = checkDayMonth("this_month")#aqui filtro mes
    dt_start = dt_now["dt_start"]
    dt_end = dt_now["dt_end"]
    with connections['customer_refer'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.tel1_p, b.tipo_servico, c.tipo_exame, e.nome, a.resp_medico, a.data_agendamento, a.status FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p WHERE a.data_agendamento BETWEEN %s AND %s"
        cursor.execute(query, (dt_start, dt_end,))
        dados = cursor
        array = []
        for id, paciente, phone, service, exame, nurse, doctor, data, status  in dados:
            dataFormatada = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y") if data not in ["", None] else ""
            newinfoa = ({
                "id": id,
                "paciente": paciente,
                "phone": phone,
                "service": service,
                "exame": exame,
                "nurse": nurse,
                "doctor": doctor,
                "date_age": dataFormatada,
                "status": status,
                })
            array.append(newinfoa)
    return array 

#MODAL COLETA AGENDADA
def SearchModalScheduled(request):
    id = request.POST.get('id_user')
    dict_response = {}

    with connections['customer_refer'].cursor() as cursor:
        params = (
            id,
        )
        query = "SELECT a.id, a.data_agendamento, a.hr_agendamento, b.tipo_servico, c.tipo_exame, g.nome_conv, e.nome, f.nome, np.nome_p, a.tel1_p, a.tel2_p, a.resp_medico, a.resp_atendimento, a. resp_comercial, a.cep, a.rua, a.numero, a.complemento, a.bairro, a.cidade, a.uf, a.val_cust, a.val_work_lab, a.val_pag, a.obs, b.tipo_servico, c.tipo_exame, a.status, a.motivo_status, co.color FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN admins.health_insurance g ON a.convenio = g.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN auth_users.users f ON a.motorista = f.id INNER JOIN admins.status_colors co ON a.status = co.status_c INNER JOIN customer_refer.patients np ON a.nome_p = np.id_p WHERE a.id = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for a_id, a_data_agendamento, a_hr_agendamento, b_tipo_servico, c_tipo_exame, g_nome_conv, e_nome, f_nome, a_nome_p, a_tel1_p, a_tel2_p, a_resp_medico, a_resp_atendimento, a_resp_comercial, a_cep, a_rua, a_numero, a_complemento, a_bairro, a_cidade, a_uf, a_val_cust, a_val_work_lab, a_val_pag, a_obs, b_tipo_servico, c_tipo_exame, a_status, a_msotivo_tatus, co_color in dados:
                dict_response = {
                    "agendamento": {
                        "data_agendamento": a_data_agendamento,
                        "hr_agendamento": a_hr_agendamento,
                        "tipo_servico": b_tipo_servico,
                        "tipo_exame": c_tipo_exame,
                        "motorista": e_nome,
                        "nurse": f_nome,
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
                    },
                    "obs": {
                        "obs": a_obs,
                        "statusM": a_status,
                        "motivo_status": a_msotivo_tatus,
                        "color": co_color,


                    },
                } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
    
    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }


#ATUALIZAR STATUS DO AGENDAMENTO CONCLUIDO
def FunctionStatusAgendaConc(request):
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

            query2 = "INSERT INTO `auth_finances`.`completed_exams` (`id`, `id_paciente_f`, `status_exame_f`, `data_registro_f`) VALUES (NULL, %s, '8', %s);"
            cursor.execute(query2, param2)
            
            query3 = "INSERT INTO `admins`.`register_actions` (`id_register`, `id_pagina`, `tp_operacao`, `id_user`, `descriocao`, `data_operacao`) VALUES (NULL, NULL, 'salvar', %s, 'Usuario salvou o modal', %s)"
            cursor.execute(query3, (
                id_usuario,
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            ))

    #"true" -> STRING
    #true -> BOOLEAN
    return {"response": "true", "message": "Ok"}


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
    data_atual = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


    with connections['auth_agenda'].cursor() as cursor:
        params = (
            tel1, tel2, data_agendar,  hr_age, zipcode, addres, number, complement, district, city, uf, cust_alv, obs, motivo_status, data_atual, id,
        )
        #query = "UPDATE auth_agenda.collection_schedule SET data_agendamento = %s WHERE id = %s"
        query = "UPDATE `auth_agenda`.`collection_schedule` SET `tel1_p` = %s, `tel2_p` = %s, `data_agendamento` = %s, `hr_agendamento` = %s, `cep` = %s, `rua` = %s, `numero` = %s, `complemento` = %s, `bairro` = %s, `cidade` = %s, `uf` = %s, `val_cust` = %s, `obs` = %s, `status` = 'Pendente', motivo_status = %s,  data_fin = %s  WHERE (`id` = %s);"

        cursor.execute(query, params)

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
        query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_fin, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_paciente_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND spa.status_p  NOT LIKE  'Cancelado' AND spa.status_p  NOT LIKE  'Finalizado';"
        cursor.execute(query)
        dados = cursor
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


#SELECT STATUS PROCESSO
def FunctionStatus(request):
    with connections['auth_finances'].cursor() as cursor:
        query = "SELECT * FROM auth_finances.status_progress;"
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
    id = request.POST.get("id_user")

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

        print(date_create, id, id_usuario)
        param = (date_create, id_usuario, id,)
        query = "UPDATE `auth_finances`.`completed_exams` SET `data_inc_proc_f` = %s, `status_exame_f` = '1', `resp_inicio_p_f` = %s WHERE (`id_paciente_f` = %s);"

        cursor.execute(query, param)
        
    
    return {"response": "true", "message": "Processo Financeiro iniciado!"}


#MODAL COLETA AGENDADA CONCLUIDA
def SearchModalExamsFunction(request):
    id = request.POST.get('id_user')
    
    FC = FinancesExams()
    dict_response = {}
    modal_data = FC.schedule_collection(id)
    finances_exams_data = FC.fetch_exams(id)

    dict_response.update(modal_data) if modal_data else None
    dict_response.update(finances_exams_data) if modal_data else None

    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MESSAGE COM O DICT 
    }

