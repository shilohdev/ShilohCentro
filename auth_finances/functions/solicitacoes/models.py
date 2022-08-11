

from django.db import connections
from functions.general.decorator import convertDate, fetchAdministrator

class SolicitacaoReembolso:

    def __init__(self, perfil=None, unityY=None):
        self.perfil = perfil
        self.unityY = unityY


    def Solicitacao_Reembolso_Pendente_Function(perfil, unityY):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unityY)
            query = "SELECT DISTINCT a.id_agendamento_f, unit.data_agendamento, a.regis, ex.tipo_exame, und.unit_s, und.id_unit_s, st.status_p, pa.nome_p, a.company FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress st ON a.status_exame_f LIKE st.id INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f INNER JOIN admins.exam_type ex ON unit.tp_exame = ex.id INNER JOIN admins.units_shiloh und ON und.id_unit_s = unit.unity INNER JOIN customer_refer.patients pa ON unit.nome_p = pa.id_p WHERE {} AND a.identification LIKE 'Externo' AND unit.status like 'Concluído' AND a.status_exame_f LIKE 8 OR a.status_exame_f LIKE 4 AND a.regis LIKE 0 ORDER BY unit.data_agendamento ASC".format(Q)
            cursor.execute(query)
            dados = cursor
            array = []

            for id_agendamento, data_agendamento, regis, exame, unidade, id_unidade, status, nome_paciente, company in dados:
                newinfoa = ({
                    "id": id_agendamento,
                    "paciente": nome_paciente,
                    "dataconc": convertDate(data_agendamento),
                    "exame": exame,
                    "status_p": status,
                    "unidade": unidade,
                    "id_unidade": id_unidade,
                    "regis": regis,
                    "company": company,
                    "contrato": "",
                })
                array.append(newinfoa)
            return array


    def Solicitacao_Reembolso_Andamento_Function(perfil, unityY):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unityY)
            query = "SELECT DISTINCT a.id_agendamento_f, unit.data_agendamento, a.regis, ex.tipo_exame, und.unit_s, und.id_unit_s, st.status_p, pa.nome_p, a.company FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress st ON a.status_exame_f LIKE st.id INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f INNER JOIN admins.exam_type ex ON unit.tp_exame = ex.id INNER JOIN admins.units_shiloh und ON und.id_unit_s = unit.unity INNER JOIN customer_refer.patients pa ON unit.nome_p = pa.id_p WHERE {} AND a.identification LIKE 'Externo' AND unit.status like 'Concluído' AND a.status_exame_f LIKE 1 OR a.status_exame_f LIKE 2 AND a.regis LIKE 0 ORDER BY unit.data_agendamento ASC".format(Q)
            cursor.execute(query)
            dados = cursor
            array = []

            for id_agendamento, data_agendamento, regis, exame, unidade, id_unidade, status, nome_paciente, company in dados:
                newinfoa = ({
                    "id": id_agendamento,
                    "paciente": nome_paciente,
                    "dataconc": convertDate(data_agendamento),
                    "exame": exame,
                    "status_p": status,
                    "unidade": unidade,
                    "id_unidade": id_unidade,
                    "regis": regis,
                    "company": company,
                    "contrato": "",
                })
                array.append(newinfoa)
            return array

    def Solicitacao_Reembolso_Glosa_Natingido_Function(perfil, unityY):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unityY)
            query = "SELECT DISTINCT a.id_agendamento_f, unit.data_agendamento, a.regis, ex.tipo_exame, und.unit_s, und.id_unit_s, st.status_p, pa.nome_p, a.company FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress st ON a.status_exame_f LIKE st.id INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f INNER JOIN admins.exam_type ex ON unit.tp_exame = ex.id INNER JOIN admins.units_shiloh und ON und.id_unit_s = unit.unity INNER JOIN customer_refer.patients pa ON unit.nome_p = pa.id_p WHERE {} AND unit.status like 'Concluído' AND a.status_exame_f LIKE 5 OR a.status_exame_f LIKE 6 AND a.regis LIKE 0 AND a.identification LIKE 'Externo'ORDER BY unit.data_agendamento ASC".format(Q)
            cursor.execute(query)
            dados = cursor
            array = []

            for id_agendamento, data_agendamento, regis, exame, unidade, id_unidade, status, nome_paciente, company in dados:
                newinfoa = ({
                    "id": id_agendamento,
                    "paciente": nome_paciente,
                    "dataconc": convertDate(data_agendamento),
                    "exame": exame,
                    "status_p": status,
                    "unidade": unidade,
                    "id_unidade": id_unidade,
                    "regis": regis,
                    "company": company,
                    "contrato": "",
                })
                array.append(newinfoa)
            return array


    def Solicitacao_Reembolso_Finalizado_Function(perfil, unityY):
        with connections['auth_agenda'].cursor() as cursor:
            Q = fetchAdministrator("a.unity", perfil, unityY)
            query = "SELECT a.id, pa.nome_p, a.data_fin, sp.data_inc_proc_f, sp.data_final_f, ex.tipo_exame, spa.status_p, uni.unit_s FROM auth_agenda.collection_schedule a INNER JOIN customer_refer.patients pa ON a.nome_p = pa.id_p INNER JOIN auth_finances.completed_exams sp ON a.id = sp.id_agendamento_f INNER JOIN auth_finances.status_progress spa ON spa.id = sp.status_exame_f INNER JOIN  admins.exam_type ex ON a.tp_exame = ex.id INNER JOIN  admins.units_shiloh uni ON a.unity = uni.id_unit_s WHERE {} AND a.status = 'Concluído' AND sp.regis LIKE  '1';".format(Q)
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


    def Qtd_Total_Solicitacoes_Reemboslo(perfil, unity):
        """ Quantidade total das solicitações de reembolso """
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)
            query = "SELECT distinct a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress st ON a.status_exame_f LIKE st.id INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.status_exame_f NOT LIKE 9 AND a.regis LIKE 0 AND a.identification LIKE 'Externo'".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            qtd = 0
            if not dados:
                qtd
            else:
                for i in dados: 
                    qtd += 1 
            array.append({"qtd": qtd})
            return array


    def Dash_Solicitacao_Reembolso_Pendente(perfil, unity):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)

            query = "SELECT DISTINCT a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.identification LIKE 'Externo' AND a.status_exame_f LIKE 8 AND a.regis LIKE 0".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            pendentes = 0
            if not dados:
                pendentes
            else:
                for i in dados: 
                    pendentes += 1 
            array.append({"pendentes": pendentes})
            return array


    def Dash_Solicitacao_Reembolso_Pago(perfil, unity):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)

            query = "SELECT DISTINCT a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.identification LIKE 'Externo' AND a.status_exame_f LIKE 4 AND a.regis LIKE 0".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            pago = 0
            if not dados:
                pago
            else:
                for i in dados: 
                    pago += 1 
            array.append({"pago": pago})
            return array



    def Dash_Solicitacao_Reembolso_Andamento(perfil, unity):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)

            query = "SELECT DISTINCT a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.identification LIKE 'Externo' AND a.status_exame_f LIKE 1 AND a.regis LIKE 0 ".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            andamento = 0
            if not dados: 
                andamento
            else: 
                for i in dados: 
                    andamento += 1 
            array.append({"andamento": andamento})
            return array


    def Dash_Solicitacao_Reembolso_Analise(perfil, unity):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)

            query = "SELECT DISTINCT a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.identification LIKE 'Externo' AND a.status_exame_f LIKE 2  AND a.regis LIKE 0".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            analise = 0
            if not dados: 
                analise
            else: 
                for i in dados: 
                    analise += 1 
            array.append({"analise": analise})
            return array


    def Dash_Solicitacao_Reembolso_Glosa(perfil, unity):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)

            query = "SELECT DISTINCT a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.identification LIKE 'Externo' AND a.status_exame_f LIKE 5 AND a.regis LIKE 0 ".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            glosa = 0
            if not dados: 
                glosa
            else: 
                for i in dados: 
                    glosa += 1 
            array.append({"glosa": glosa})
            return array

    def Dash_Solicitacao_Reembolso_Nao_Atingido(perfil, unity):
        with connections['auth_finances'].cursor() as cursor:
            Q = fetchAdministrator("unit.unity", perfil, unity)

            query = "SELECT DISTINCT a.id_agendamento_f FROM auth_finances.completed_exams a INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f WHERE {} AND a.identification LIKE 'Externo' AND a.status_exame_f LIKE 6 AND a.regis LIKE 0".format(Q)
            cursor.execute(query)
            dados = cursor.fetchall()
            array = []
            nao_atingido = 0
            if not dados: 
                nao_atingido
            else: 
                for i in dados: 
                    nao_atingido += 1 
            array.append({"nao_atingido": nao_atingido})
            return array