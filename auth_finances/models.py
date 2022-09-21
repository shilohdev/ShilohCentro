from datetime import datetime
import imp
import json
from django.db import models
from django.db import connections
import base64
from functions.general.decorator import convertDate


class DashPartners_Closing:
    def __init__(self, mes=None, ano=None) -> None:
        self.mes = mes
        self.ano = ano


    def PagosLabMovel(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano}  AND status_partners LIKE 'Pago' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Lab Movel'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_medico, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array

    def PagosShilohLab(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_partners LIKE 'Pago' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Shiloh Lab'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_medico, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})
            
            return array

    def APagarLabMovel(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_partners LIKE 'Pendente' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Lab Movel'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_medico, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array

    
    def APagarShilohLab(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_partners LIKE 'Pendente' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Shiloh Lab'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_medico, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array


    def Total(self):        
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT COUNT(DISTINCT id_agendamento) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano}  AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
            cursor.execute(querys)
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
            else:
                newinfoa = ({
                    "qdt": "0",
                    "val": "R$ 00,00",
                    "mes": "0",
                    })
                array2.append(newinfoa)
                return array2


    def FiltroTable(self):
     with connections['auth_finances'].cursor() as cursor:
        query = f"SELECT b.id, b.nome, c.categoria, co.nome, b.rn, month(a.data_repasse) AS mes_repasse, YEAR( a.data_repasse), SUM(a.valor_uni_partners) AS total, a.status_partners, a.relacao_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id INNER JOIN auth_users.users co ON a.nome_comercial = co.id INNER JOIN auth_users.Category_pertners c ON b.categoria = c.id WHERE EXTRACT(MONTH FROM a.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM a.data_repasse) = {self.ano} GROUP BY a.nome_medico, co.nome, b.rn, MONTH( a.data_repasse), YEAR( a.data_repasse), b.id, a.status_partners, a.relacao_partners"
        cursor.execute(query)
        dadoss = cursor.fetchall()
        array = []
        if dadoss:
            for id, medico, categoria, comercial, rn, mes, ano, valor, status, company in dadoss:
                mes_ref = str(mes) + '/' + str(ano)
                print(mes_ref)
                valor = (valor) if valor not in ["", None] else None
                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "id": id,
                    "medico": medico,
                    "rn": rn, 
                    "categoria": categoria,
                    "comercial": comercial,
                    "mes": mes_ref,
                    "valor": valor,
                    "status": status,
                    "company": company,
                    })
                array.append(newinfoa)
        else:
            return False
        
        return array


class DashCommerce_Closing:
    def __init__(self, mes=None, ano=None) -> None:
        self.mes = mes
        self.ano = ano

    def Commerce_PagosLabMovel(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_commerce, nome_comercial, status_comercial, valor_comercial FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_comercial LIKE 'Pago' AND valor_comercial NOT LIKE '0' AND relacao_commerce like 'Lab Movel'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_comercial, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array

    def Commerce_PagosShilohLab(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_commerce, nome_comercial, status_comercial, valor_comercial FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_comercial LIKE 'Pago' AND valor_comercial NOT LIKE '0' AND relacao_commerce like 'Shiloh Lab'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_comercial, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})
            
            return array

    def Commerce_ApagarLabMovel(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_commerce, nome_comercial, status_comercial, valor_comercial FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_comercial LIKE 'Pendente' AND valor_comercial NOT LIKE '0' AND relacao_commerce like 'Lab Movel'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_comercial, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array

    
    def Commerce_ApagarShilohLab(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT relacao_commerce, nome_comercial, status_comercial, valor_comercial FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_comercial LIKE 'Pendente' AND valor_comercial NOT LIKE '0' AND relacao_commerce like 'Shiloh Lab'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for relacao, id_comercial, status, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array


    def Commerce_Total(self):        
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT COUNT(DISTINCT id_agendamento) AS contagem, SUM(valor_comercial) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano}  AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
            cursor.execute(querys)
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
            else:
                newinfoa = ({
                    "qdt": "0",
                    "val": "R$ 00,00",
                    "mes": "0",
                    })
                array2.append(newinfoa)
                return array2


    def Commerce_FiltroTable(self):
     with connections['auth_finances'].cursor() as cursor:
        query = f"SELECT b.id, b.nome, month( a.data_repasse), a.status_comercial, a.relacao_commerce, SUM(a.valor_comercial) AS total FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_comercial = b.id WHERE a.valor_comercial NOT LIKE '0' AND EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND b.nome NOT LIKE 'Tosyn Lopes'  GROUP BY b.id, b.nome, MONTH( a.data_repasse), a.status_comercial, a.valor_comercial, a.relacao_commerce"
        cursor.execute(query)
        dadoss = cursor.fetchall()
        array = []
        if dadoss:
            for id, comercial, mes, status, company, valor in dadoss:
                valor = (valor) if valor not in ["", None] else None
                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                newinfoa = ({
                    "id": id,
                    "nome": comercial,
                    "mes": mes,
                    "valor": valor,
                    "status": status,
                    "company": company,
                    })
                array.append(newinfoa)
        else:
            return False
        
        return array



class DashInterno_Closing:
    def __init__(self, mes=None, ano=None) -> None:
        self.mes = mes
        self.ano = ano

    def Interno_PagosLabMovel(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT finance.nome_medico, finance.valor_uni_partners FROM auth_finances.closing_finance finance INNER JOIN auth_users.users us ON finance.nome_medico = us.id WHERE us.perfil != 7 AND EXTRACT(MONTH FROM finance.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM finance.data_repasse) = {self.ano} AND finance.valor_comercial LIKE '0' AND finance.status_partners LIKE 'Pago' AND finance.relacao_commerce like 'Lab Movel'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for id_medico, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array

    def Interno_PagosShilohLab(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT finance.nome_medico, finance.valor_uni_partners FROM auth_finances.closing_finance finance INNER JOIN auth_users.users us ON finance.nome_medico = us.id WHERE us.perfil != 7 AND EXTRACT(MONTH FROM finance.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM finance.data_repasse) = {self.ano} AND finance.valor_comercial LIKE '0' AND finance.status_partners LIKE 'Pago' AND finance.relacao_commerce like 'Shiloh Lab'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for id_medico, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})
            
            return array

    def Interno_ApagarLabMovel(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT finance.nome_medico, finance.valor_uni_partners FROM auth_finances.closing_finance finance INNER JOIN auth_users.users us ON finance.nome_medico = us.id WHERE us.perfil != 7 AND EXTRACT(MONTH FROM finance.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM finance.data_repasse) = {self.ano} AND finance.valor_comercial LIKE '0' AND finance.status_partners LIKE 'Pendente' AND finance.relacao_commerce like 'Lab Movel'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for id_medico, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array

    
    def Interno_ApagarShilohLab(self):
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT finance.nome_medico, finance.valor_uni_partners FROM auth_finances.closing_finance finance INNER JOIN auth_users.users us ON finance.nome_medico = us.id WHERE us.perfil != 7 AND EXTRACT(MONTH FROM finance.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM finance.data_repasse) = {self.ano} AND finance.valor_comercial LIKE '0' AND finance.status_partners LIKE 'Pendente' AND finance.relacao_commerce like 'Shiloh Lab'"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                valor = [(valor) for id_medico, valor in dados]
                valor = sum(valor)

                valor = f"R$ {valor:_.2f}"
                valor = valor.replace(".", ",").replace("_", ".")
                
                array.append({"valor": valor})

            else:
                array.append({"valor": "R$ 00,00"})

            return array


    def Interno_Total(self):        
        with connections['auth_finances'].cursor() as cursor:
            querys = f"SELECT COUNT(DISTINCT id_agendamento) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano}  AND valor_comercial LIKE '0' group by MONTH(data_repasse)"
            cursor.execute(querys)
            dados = cursor.fetchall()
            array = []
            if dados:
                for qdt, val, mes in dados:
                    val = f"R$ {val:_.2f}"
                    val = val.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "qdt": qdt,
                        "val": val,
                        "mes": mes,
                        })
                    array.append(newinfoa)
                    return array
            else:
                newinfoa = ({
                    "qdt": "0",
                    "val": "R$ 00,00",
                    "mes": "0",
                    })
                array.append(newinfoa)
                return array


    def Interno_FiltroTable(self):
        with connections['auth_finances'].cursor() as cursor:
            query = f"SELECT a.nome_medico, b.nome, a.status_partners, SUM(a.valor_uni_partners), a.relacao_commerce FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id WHERE a.valor_comercial LIKE '0' AND EXTRACT(MONTH FROM a.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM a.data_repasse) = {self.ano} GROUP BY a.nome_medico, b.nome, a.status_partners, MONTH(a.data_repasse), a.relacao_commerce"
            cursor.execute(query)
            dadoss = cursor.fetchall()
            array = []
            if dadoss:
                for id, nome, status_partners, valor, company in dadoss:
                    valor = (valor) if valor not in ["", None] else None
                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "id": id,
                        "nome": nome,
                        "status": status_partners,
                        "valor": valor,
                        "company": company,
                        })
                    array.append(newinfoa)
            else:
                return False
            
            return array



#filtro personalizado dos parceiros
class ClosingPartnersFilter:
    def __init__(self, data_inicio, data_fim):
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    '''
        def PagosLabMovel(self):
            with connections['auth_finances'].cursor() as cursor:
                querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano}  AND status_partners LIKE 'Pago' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Lab Movel'"
                cursor.execute(querys)
                dados = cursor.fetchall()
                array = []
                if dados:
                    valor = [(valor) for relacao, id_medico, status, valor in dados]
                    valor = sum(valor)

                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    
                    array.append({"valor": valor})

                else:
                    array.append({"valor": "R$ 00,00"})

                return array

        def PagosShilohLab(self):
            with connections['auth_finances'].cursor() as cursor:
                querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_partners LIKE 'Pago' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Shiloh Lab'"
                cursor.execute(querys)
                dados = cursor.fetchall()
                array = []
                if dados:
                    valor = [(valor) for relacao, id_medico, status, valor in dados]
                    valor = sum(valor)

                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    
                    array.append({"valor": valor})

                else:
                    array.append({"valor": "R$ 00,00"})
                
                return array

        def APagarLabMovel(self):
            with connections['auth_finances'].cursor() as cursor:
                querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_partners LIKE 'Pendente' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Lab Movel'"
                cursor.execute(querys)
                dados = cursor.fetchall()
                array = []
                if dados:
                    valor = [(valor) for relacao, id_medico, status, valor in dados]
                    valor = sum(valor)

                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    
                    array.append({"valor": valor})

                else:
                    array.append({"valor": "R$ 00,00"})

                return array

        
        def APagarShilohLab(self):
            with connections['auth_finances'].cursor() as cursor:
                querys = f"SELECT relacao_partners, nome_medico, status_partners, valor_uni_partners FROM auth_finances.closing_finance where EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano} AND status_partners LIKE 'Pendente' AND valor_comercial NOT LIKE '0' AND relacao_partners like 'Shiloh Lab'"
                cursor.execute(querys)
                dados = cursor.fetchall()
                array = []
                if dados:
                    valor = [(valor) for relacao, id_medico, status, valor in dados]
                    valor = sum(valor)

                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    
                    array.append({"valor": valor})

                else:
                    array.append({"valor": "R$ 00,00"})

                return array


        def Total(self):        
            with connections['auth_finances'].cursor() as cursor:
                querys = f"SELECT COUNT(DISTINCT id_agendamento) AS contagem, SUM(valor_uni_partners) AS total, MONTH(data_repasse) FROM auth_finances.closing_finance WHERE EXTRACT(MONTH FROM data_repasse) = {self.mes} AND EXTRACT(YEAR FROM data_repasse) = {self.ano}  AND valor_comercial NOT LIKE '0' group by MONTH(data_repasse)"
                cursor.execute(querys)
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
                else:
                    newinfoa = ({
                        "qdt": "0",
                        "val": "R$ 00,00",
                        "mes": "0",
                        })
                    array2.append(newinfoa)
                    return array2
    '''

    def FiltroTable(self):
        with connections['auth_finances'].cursor() as cursor:
            queryCalculo = f"SELECT b.id, b.nome, c.categoria, co.nome, b.rn, month(a.data_repasse), YEAR( a.data_repasse), SUM(a.valor_uni_partners) AS total, a.status_partners, a.relacao_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id INNER JOIN auth_users.users co ON a.nome_comercial = co.id INNER JOIN auth_users.Category_pertners c ON b.categoria = c.id WHERE a.data_repasse BETWEEN '{self.data_inicio}' and '{self.data_fim}' GROUP BY a.nome_medico, co.nome, b.rn, month(a.data_repasse), YEAR( a.data_repasse), b.id, a.status_partners, a.relacao_partners"
            cursor.execute(queryCalculo)
            dados = cursor.fetchall()
            array = []
            if dados:
                for id, medico, categoria, comercial, rn, mes, ano, valor, status, company in dados:
                    mes_ref = str(mes) + '/' + str(ano)
                    valor = (valor) if valor not in ["", None] else None
                    valor = f"R$ {valor:_.2f}"
                    valor = valor.replace(".", ",").replace("_", ".")
                    newinfoa = ({
                        "id": id,
                        "medico": medico,
                        "rn": rn, 
                        "categoria": categoria,
                        "comercial": comercial,
                        "mes": mes_ref,
                        "valor": valor,
                        "status": status,
                        "company": company,
                        })
                    array.append(newinfoa)
            else:
                return False
            
            return array



class ClosingPartnersModal_Mes:
    def __init__(self, mes=None, id_medico=None) -> None:
        self.mes = mes
        self.id_medico = id_medico

    def relacao_pagos(self):
        with connections['auth_agenda'].cursor() as cursor:
            queryPago = "SELECT nome_medico, nome_paciente, data_coleta, data_repasse, exame, valor_uni_partners FROM auth_finances.closing_finance WHERE MONTH(data_repasse) = '{}' AND nome_medico = '{}'".format(self.mes, self.id_medico)
            cursor.execute(queryPago)
            dados = cursor.fetchall()
            arrayPago = []
            if dados: 
                for iDmedico, pacienteP,  dataColetaP, dataRepasseP, exameP, valor_uniP in dados:
                    valor_uniP = f"R$ {valor_uniP:_.2f}"
                    valor_uniP = valor_uniP.replace(".", ",").replace("_", ".")

                    newinfoa = ({
                        "iDmedico": iDmedico,
                        "pacienteP": pacienteP,
                        "dataColetaP": convertDate(dataColetaP),
                        "dataRepasseP": convertDate(dataRepasseP),
                        "exameP": exameP,
                        "valor_uniP": valor_uniP,
                        })
                    arrayPago.append(newinfoa)
            else:
                newinfoa = ({
                    "iDmedico": '-',
                    "pacienteP": '-',
                    "dataColetaP": '-',
                    "dataRepasseP": '-',
                    "exameP": '-',
                    "valor_uniP": '-',
                    })
                arrayPago.append(newinfoa)

            return arrayPago 

            

    def count_pagos(self):
        with connections['auth_agenda'].cursor() as cursor:
            queryCount = "SELECT COUNT(*) AS contagem, SUM(valor_uni_partners) AS total FROM auth_finances.closing_finance WHERE MONTH(data_repasse) = '{}' AND nome_medico = '{}'".format(self.mes, self.id_medico)
            cursor.execute(queryCount)
            dados = cursor.fetchall()
            arrayPagoCount = []
            if dados:
                for contagem, valor in dados:
                    if valor == None:
                        valor = 0
                    valor = float(valor) if valor not in ["", None] else None
                    valor = f"R$ {valor:_.2f}"
                    valorS = valor.replace(".", ",").replace("_", ".")

                    newinfoa = ({
                        "contagem": contagem,
                        "valor": valorS,
                        })
                    arrayPagoCount.append(newinfoa)
            else:
                newinfoa = ({
                    "contagem": '-',
                    "valor": '-',
                    })
                arrayPagoCount.append(newinfoa)


            return arrayPagoCount

    
    def analise(self):
        with connections['auth_agenda'].cursor() as cursor:
            queryPago = "SELECT us.id, pa.nome_p, ex.tipo_exame, ag.data_agendamento FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f WHERE us.id = '{}' AND ff.status_exame_f LIKE 2".format(self.id_medico)
            cursor.execute(queryPago)
            dados = cursor.fetchall()
            arrayAnalise = []
            if dados: 
                for id, nome_p, tipo_exame, data_agendamento in dados:

                    newinfoa = ({
                        "id": id,
                        "nome_p": nome_p,
                        "tipo_exame": tipo_exame,
                        "data_agendamento": convertDate(data_agendamento),
                        })
                    arrayAnalise.append(newinfoa)
            else:
                newinfoa = ({
                    "nome_p": '-',
                    "tipo_exame": '-',
                    "data_agendamento": '-',
                    })
                arrayAnalise.append(newinfoa)
            return arrayAnalise

    def GlosaNaoAtingido(self):
        print(self.id_medico)
        with connections['auth_agenda'].cursor() as cursor:
            queryPago = "SELECT us.id, pa.nome_p, ex.tipo_exame, ag.data_agendamento, exm.status_p FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f INNER JOIN auth_finances.status_progress exm ON ff.status_exame_f = exm.id WHERE us.id = '{}' AND ff.status_exame_f LIKE 6 OR ff.status_exame_f LIKE 5".format(self.id_medico)
            cursor.execute(queryPago)
            dados = cursor.fetchall()
            array = []
            if dados:
                print("a")
                for id, nome_p, tipo_exame, data_agendamento, status in dados:
                    newinfoa = ({
                        "id": id,
                        "nome_p": nome_p,
                        "tipo_exame": tipo_exame,
                        "data_agendamento": convertDate(data_agendamento),
                        "status": status,
                        })
                    array.append(newinfoa)
            else:
                newinfoa = ({
                    "nome_p": '-',
                    "tipo_exame": '-',
                    "data_agendamento": '-',
                    "status": '-',
                    })
                array.append(newinfoa)
            return array


    def Repasse(self):
        with connections['auth_agenda'].cursor() as cursor:
            queryPago = "SELECT us.id, pa.nome_p, ex.tipo_exame, ag.data_agendamento, exm.status_p FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f INNER JOIN auth_finances.status_progress exm ON ff.status_exame_f = exm.id WHERE us.id = '{}' AND ff.status_exame_f LIKE 12".format(self.id_medico)
            cursor.execute(queryPago)
            dados = cursor.fetchall()
            array = []
            if dados: 
                for id, nome_p, tipo_exame, data_agendamento, status in dados:
                    newinfoa = ({
                        "id": id,
                        "nome_p": nome_p,
                        "tipo_exame": tipo_exame,
                        "data_agendamento": convertDate(data_agendamento),
                        })
                    array.append(newinfoa)
            else:
                newinfoa = ({
                    "nome_p": '-',
                    "tipo_exame": '-',
                    "data_agendamento": '-',
                    })
                array.append(newinfoa)
            return array


    def GlosaNaoAtingido(self):
        with connections['auth_agenda'].cursor() as cursor:
            queryPago = "SELECT us.id, pa.nome_p, ex.tipo_exame, ag.data_agendamento FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f INNER JOIN auth_finances.status_progress exm ON ff.status_exame_f = exm.id WHERE us.id = '{}' AND ff.status_exame_f LIKE 13".format(self.id_medico)
            cursor.execute(queryPago)
            dados = cursor.fetchall()
            array = []
            if dados: 
                for id, nome_p, tipo_exame, data_agendamento in dados:
                    newinfoa = ({
                        "id": id,
                        "nome_p": nome_p,
                        "tipo_exame": tipo_exame,
                        "data_agendamento": convertDate(data_agendamento),
                        })
                    array.append(newinfoa)
            else:
                newinfoa = ({
                    "nome_p": '-',
                    "tipo_exame": '-',
                    "data_agendamento": '-',
                    })
                array.append(newinfoa)
            return array


    def Outros(self):
        with connections['auth_agenda'].cursor() as cursor:
            queryPago = "SELECT us.id, pa.nome_p, ex.tipo_exame, ag.data_agendamento, exm.status_p FROM auth_agenda.collection_schedule ag INNER JOIN customer_refer.patients pa ON ag.nome_p = pa.id_p INNER JOIN auth_users.users us ON pa.medico_resp_p = us.id INNER JOIN admins.exam_type ex ON ex.id = ag.tp_exame INNER JOIN auth_finances.completed_exams ff ON ag.id = ff.id_agendamento_f INNER JOIN auth_finances.status_progress exm ON ff.status_exame_f = exm.id WHERE us.id = '{}' AND ff.status_exame_f LIKE 6 OR ff.status_exame_f LIKE 5".format(self.id_medico)
            cursor.execute(queryPago)
            dados = cursor.fetchall()
            array = []
            if dados: 
                for id, nome_p, tipo_exame, data_agendamento, status in dados:
                    newinfoa = ({
                        "id": id,
                        "nome_p": nome_p,
                        "tipo_exame": tipo_exame,
                        "data_agendamento": convertDate(data_agendamento),
                        "status": status,
                        })
                    array.append(newinfoa)
            else:
                newinfoa = ({
                    "nome_p": '-',
                    "tipo_exame": '-',
                    "data_agendamento": '-',
                    "status": '-',
                    })
                array.append(newinfoa)
            return array 