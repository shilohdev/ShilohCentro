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
from functions.connection.models import Connection, Exams
from functions.general.decorator import convertDate
from django.forms import model_to_dict


class FinancesExams:
    def __init__(self) -> None:
        self.cursor = Connection('userdb', '', '', '', '').connection()

    def schedule_collection(self, id):
        cursor = self.cursor
        params = (
            id,
        )
        query = "SELECT a.id, a.data_agendamento, a.hr_agendamento, b.tipo_servico, c.tipo_exame, g.nome_conv, e.nome, f.nome, np.nome_p, a.tel1_p, a.tel2_p, a.resp_medico, a.resp_atendimento, a. resp_comercial, a.cep, a.rua, a.numero, a.complemento, a.bairro, a.cidade, a.uf, a.val_cust, a.val_work_lab, a.val_pag, a.obs, b.tipo_servico, c.tipo_exame, a.status, a.motivo_status, co.color FROM auth_agenda.collection_schedule a INNER JOIN admins.type_services b ON a.tp_servico = b.id INNER JOIN admins.exam_type c ON a.tp_exame = c.id INNER JOIN admins.health_insurance g ON a.convenio = g.id INNER JOIN auth_users.users e ON a.resp_enfermeiro = e.id INNER JOIN auth_users.users f ON a.motorista = f.id INNER JOIN admins.status_colors co ON a.status = co.status_c INNER JOIN customer_refer.patients np ON a.nome_p = np.id_p WHERE a.id = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for a_id, a_data_agendamento, a_hr_agendamento, b_tipo_servico, c_tipo_exame, g_nome_conv, e_nome, f_nome, a_nome_p, a_tel1_p, a_tel2_p, a_resp_medico, a_resp_atendimento, a_resp_comercial, a_cep, a_rua, a_numero, a_complemento, a_bairro, a_cidade, a_uf, a_val_cust, a_val_work_lab, a_val_pag, a_obs, b_tipo_servico, c_tipo_exame, a_status, a_msotivo_tatus, co_color in dados:
                return {
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
                        "date_frist": a_val_pag,
                    },
                    "obs": {
                        "obs": a_obs,
                        "statusM": a_status,
                        "motivo_status": a_msotivo_tatus,
                        "color": co_color,

                    }
                }
        
        return None

    def fetch_exams(self, id):
        cursor = self.cursor

        params = (
            id,
        )
        query = "SELECT data_inc_proc_f, status_exame_f, resp_inicio_p_f, data_final_f FROM auth_finances.completed_exams WHERE id_paciente_f = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
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
        
        return None


#MODAL COLETA AGENDADA
def FunctionModalFinances(request):
    id = request.POST.get('id_user')
    dict_response = {}
    with connections['auth_finances'].cursor() as cursor:
        params = (
            id,
        )
        query = "SELECT ef.id, ef.id_paciente_f, ef.data_inc_proc_f, ef.status_exame_f, sf.status_p, ur.nome, ef.val_alvaro_f, ef.val_work_f, ef.val_pag_f, ef.porcentagem_paga_f, ef.data_repasse, ef.nf_f, ef.anx_f, ef.data_aquivo_f, ef.data_final_f, ef.data_registro_f, ef.resp_final_p_f FROM auth_finances.completed_exams ef INNER JOIN auth_users.users ur ON ef.resp_inicio_p_f = ur.id INNER JOIN auth_finances.status_progress sf ON ef.status_exame_f = sf.id WHERE ef.id_paciente_f = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()
        if dados:
            for ef_id, ef_id_paciente_f, ef_data_inc_proc_f, ef_status_exame_f_id, ef_status_exame_f, ur_nome, ef_val_alvaro_f, ef_val_work_f, ef_val_pag_f, ef_porcentagem_paga_f, ef_data_repasse,  ef_nf_f, ef_anx_f, ef_data_aquivo_f, ef_data_final_f, ef_data_registro_f, ef_resp_final_p_f in dados:
                dict_response = {
                    "dados": {
                        "id": ef_id, # id da linha
                        "pacient": ef_id_paciente_f, # paciente
                        "date_start": convertDate(ef_data_inc_proc_f), #dia que começou o processo
                        "status_process": ef_status_exame_f,# status do processo
                        "status_process_id": ef_status_exame_f_id,# status do processo
                        "resp_start": ur_nome,#responsavel por iniciar
                        "val_alvaro": ef_val_alvaro_f,# valor alvaro
                        "val_work": ef_val_work_f,# valor worklab
                        "val_pago": ef_val_pag_f,# valor pago
                        "por_paga": ef_porcentagem_paga_f,# porcentagem paga
                        "date_repasse": ef_data_repasse,# nota fiscal
                        "nf": ef_nf_f,# nota fiscal
                        "anx": ef_anx_f,# anexo
                        "date_anx": ef_data_aquivo_f,# data do anexo
                        "date_end": ef_data_final_f,# data final do processo
                        "data_regis": ef_data_registro_f,# data registro
                        "resp_end": ef_resp_final_p_f,# responsavel por finalizar
                        
                    },
                } #DICTS COM PARAMETROS PARA SEREM PASSADOS PRO JS
        else:
            dados = Exams.objects.filter(id_paciente_f=id).first()
            if dados:
                dict_response = {
                    "dados": {
                        "id": dados.id, # id da linha
                        "pacient": dados.id_paciente_f, # paciente
                        "date_start": convertDate(dados.data_inc_proc_f), #dia que começou o processo
                        "status_process": dados.status_exame_f,# status do processo
                        "resp_start": dados.resp_inicio_p_f,#responsavel por iniciar
                        "val_alvaro": dados.val_alvaro_f,# valor alvaro
                        "val_work": dados.val_work_f,# valor worklab
                        "val_pago": dados.val_pag_f,# valor pago
                        "por_paga": dados.porcentagem_paga_f,# porcentagem paga
                        "date_repasse": dados.data_repasse,# nota fiscal
                        "nf": dados.nf_f,# nota fiscal
                        "anx": dados.anx_f,# anexo
                        "date_anx": dados.data_aquivo_f,# data do anexo
                        "date_end": dados.data_final_f,# data final do processo
                        "data_regis": dados.data_registro_f,# data registro
                        "resp_end": dados.resp_final_p_f,# responsavel por finalizar
                        
                    },
                }

    return {
        "response": False if not dict_response else True,
        "message": dict_response #RETORNO DO MENSSAGE COM O DICT 
    }





#UPDATE PARCEIRO E USUARIO INTERNO
def SaveEditionsFinancesFunctions(request):
    bodyData = request.POST #var para não precisar fazer tudo um por um

    id_user = bodyData.get('id_user')
    dataKeys = { #DICT PARA PEGAR TODOS OS VALORES DO AJAX
        "tp_perfil": "perfil", #key, value >> valor que vem do ajax, valor para onde vai (banco de dados)
        "cust_alv": "val_alvaro_f",
        "val_w_lab": "val_work_f",
        "val_pago": "val_pag_f",
        "date_repass": "data_repasse",
        "n_nf": "nf_f",
        "statusProgresso": "status_exame_f",
        "porcentagem": "porcentagem_paga_f",
    }
    print(dataKeys)
    db = Connection('auth_finances', '', '', '', '')#VAR COM CONEXAO DE QUAL BANCO
    cursor = db.connection()

    for key in dataKeys:
        if key in bodyData:#SE MEU VALOR DO INPUT DO AJAX EXISTIR DENTRO DO MEU POST, FAZ A QUERY
            vData = bodyData.get(key)
            if key == "date_repass":
                vData = vData if vData not in ["", None] else None

            query = "UPDATE auth_finances.completed_exams SET {} = %s WHERE id_paciente_f = %s".format(dataKeys[key]) #format serve para aplicar o método de formatação onde possui o valor da minha var dict e colocar dentro da minha chave, para ficar no padrão de UPDATE banco
            params = (
                vData, #serve para complementar o POST e obter o valor do input
                id_user,
            )
            cursor.execute(query, params)

            print(query, params)

    return {
        "response": True,
        "message": "Dados atualizados com sucesso."
    }



#INICIO DO PROCESSO REEMBOLSO
def FinalizeProcessFunction(request):
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
        query = "UPDATE `auth_finances`.`completed_exams` SET `data_final_f` = %s, `status_exame_f` = '10', `resp_final_p_f` = %s WHERE (`id_paciente_f` = %s);"
        cursor.execute(query, param)
        print(cursor)

    
    return {"response": "true", "message": "Processo Financeiro Finalizado!"}



#REEMBOLSO FINALIZADO
def searchrRefundCompletedFunction(request):
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_fin, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_paciente_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND spa.status_p LIKE  'Finalizado';"
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


def SearchMonthExamsConclFunction(request):
    month = request.POST.get('month')
    print(month)
    with connections['auth_agenda'].cursor() as cursor:
        query = "SELECT a.id, pa.nome_p, a.resp_comercial, a.resp_medico, a.data_fin, a.status, spa.status_p FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_paciente_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f WHERE a.status = 'Concluído' AND spa.status_p  NOT LIKE  'Cancelado' AND spa.status_p  NOT LIKE  'Finalizado' AND DATE_FORMAT(a.data_fin, '%m') = %s"
        cursor.execute(query, (month,))
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

    return {
        "response": "true",
        "message": array
    }