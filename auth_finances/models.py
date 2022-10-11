from datetime import datetime
import imp
# from tkinter import Entry
from django.db import models
from django.db import connections
import base64



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
        query = f"SELECT b.id, b.nome, c.categoria, co.nome, b.rn, month( a.data_repasse) AS mes_repasse, SUM(a.valor_uni_partners) AS total, a.status_partners, a.relacao_partners FROM auth_finances.closing_finance a INNER JOIN auth_users.users b ON a.nome_medico = b.id INNER JOIN auth_users.users co ON a.nome_comercial = co.id INNER JOIN auth_users.Category_pertners c ON b.categoria = c.id WHERE EXTRACT(MONTH FROM a.data_repasse) = {self.mes} AND EXTRACT(YEAR FROM a.data_repasse) = {self.ano} GROUP BY a.nome_medico, co.nome, b.rn, MONTH( a.data_repasse), b.id, a.status_partners, a.relacao_partners"
        cursor.execute(query)
        dadoss = cursor.fetchall()
        array = []
        if dadoss:
            for id, medico, categoria, comercial, rn, data_repasse, valor, status, company in dadoss:
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

