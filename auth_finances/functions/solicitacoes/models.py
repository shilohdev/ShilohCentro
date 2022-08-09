

from django.db import connections
from functions.general.decorator import convertDate, fetchAdministrator


def Solicitacao_Reembolso_Pendente_Function(perfil, unityY):
    with connections['auth_finances'].cursor() as cursor:
        Q = fetchAdministrator("unit.unity", perfil, unityY)
        query = "SELECT DISTINCT a.id_agendamento_f, unit.data_agendamento, a.regis, ex.tipo_exame, und.unit_s, und.id_unit_s, st.status_p, pa.nome_p, a.company FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress st ON a.status_exame_f LIKE st.id INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f INNER JOIN admins.exam_type ex ON unit.tp_exame = ex.id INNER JOIN admins.units_shiloh und ON und.id_unit_s = unit.unity INNER JOIN customer_refer.patients pa ON unit.nome_p = pa.id_p WHERE {} AND a.regis LIKE 0 AND a.identification LIKE 'Externo' AND unit.status like 'Concluído' AND a.status_exame_f LIKE 8 ORDER BY unit.data_agendamento ASC".format(Q)
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


def Solicitacao_Reembolso_Andamento_Pendente_Function(perfil, unityY):
    with connections['auth_finances'].cursor() as cursor:
        Q = fetchAdministrator("unit.unity", perfil, unityY)
        query = "SELECT DISTINCT a.id_agendamento_f, unit.data_agendamento, a.regis, ex.tipo_exame, und.unit_s, und.id_unit_s, st.status_p, pa.nome_p, a.company FROM auth_finances.completed_exams a INNER JOIN auth_finances.status_progress st ON a.status_exame_f LIKE st.id INNER JOIN auth_agenda.collection_schedule unit ON unit.id = a.id_agendamento_f INNER JOIN admins.exam_type ex ON unit.tp_exame = ex.id INNER JOIN admins.units_shiloh und ON und.id_unit_s = unit.unity INNER JOIN customer_refer.patients pa ON unit.nome_p = pa.id_p WHERE {} AND a.regis LIKE 0 AND a.identification LIKE 'Externo' AND unit.status like 'Concluído' AND a.status_exame_f LIKE 1 OR a.status_exame_f LIKE 2 ORDER BY unit.data_agendamento ASC".format(Q)
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

