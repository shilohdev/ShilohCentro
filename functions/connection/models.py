from django.db import connections
from django.db import models
from functions.general.decorator import dealStrignify
from functions.connection.db import DB


class Exams(DB):
    id = models.AutoField("ID", primary_key=True, auto_created=True)
    id_paciente_f = models.IntegerField(null=True, blank=True, default=None)
    data_inc_proc_f = models.DateField("Data Inicio Processo", null=True, blank=True, default=None)
    status_exame_f = models.CharField("Status Exame", max_length=25, null=True, blank=True, default='')
    resp_inicio_p_f = models.CharField("Responsavel Inicio", max_length=25, null=True, blank=True, default='')
    val_alvaro_f = models.CharField("Valor Alvaro", max_length=25, null=True, blank=True, default='')
    val_work_f = models.CharField("Valor Work", max_length=25, null=True, blank=True, default='')
    val_pag_f = models.CharField("Valor Pagamento", max_length=25, null=True, blank=True, default='')
    porcentagem_paga_f = models.CharField("Porcentagem Paga", max_length=25, null=True, blank=True, default='')
    data_repasse = models.DateField("Data Repasse", null=True, blank=True, default=None)
    nf_f = models.CharField("Nota Fiscal", max_length=25, null=True, blank=True, default='')
    anx_f = models.CharField("Anexo Arquivos", max_length=25, null=True, blank=True, default='')
    data_aquivo_f = models.DateField("Data Arquivo", null=True, blank=True, default=None)
    data_final_f = models.DateField("Data Final", null=True, blank=True, default=None)
    data_registro_f = models.DateField("Data Registro", null=True, blank=True, default=None)
    resp_final_p_f = models.CharField("Responsavel Final", max_length=25, null=True, blank=True, default='')
    
    class Meta:
        db_table = "completed_exams"
        indexes = [
            models.Index(fields=[
                "id_paciente_f",
            ])
        ]


class Users(DB):
    id = models.AutoField("ID", primary_key=True, auto_created=True)
    perfil = models.IntegerField(null=True, blank=True, default=None)
    cpf = models.CharField("CPF", max_length=45, null=True, blank=True, default='')
    
    class Meta:
        db_table = "auth_users.users"
        indexes = [
            models.Index(fields=[
                "cpf",
            ])
        ]


class Connection:
    def __init__(self, db, table, condition, inner, params):
        self.db = db
        self.table = table
        self.conn = connections[self.db].cursor()
        self.condition = condition
        self.inner = inner
        self.params = params

    def connect(self):
        return self.conn

    def execute(self, query):
        self.conn.execute(query)
        return self.conn.fetchall()

    def insert(self, query, params=None):
        self.conn.execute(query, params) if params else self.conn.execute(query)
        return self.conn

    def fetch(self, column, params):
        if params:
            self.conn.execute("SELECT {} FROM {} {} {}".format(dealStrignify(column), self.table, self.inner, self.condition), self.params)
        else:
            self.conn.execute("SELECT {} FROM {} {} {}".format(dealStrignify(column), self.table, self.inner, self.condition))

        return self.conn.fetchall()

    def update(self, params):
        if params:
            self.conn.execute("UPDATE {} SET {}".format(self.table, self.condition), params)
        else:
            self.conn.execute("UPDATE {} SET {}".format(self.table, self.condition))

        return self.conn.rowcount

    def close(self):
        return self.conn.close()

    def connection(self):
        return connections[self.db].cursor()
        
    def execUpdate(self, table, column, condition, params):
        self.conn.execute("UPDATE {} SET {} = %s WHERE {} = %s".format(table, column, condition), params)
        return self.conn.rowcount

    def execRow(self, dictFetch, dictUpdate):
        table = dictFetch["table"]
        d_column = dictFetch["column"]
        d_condition = dictFetch["condition"]
        params = dictFetch["params"]

        column = ""
        for k in d_column.split(","):
            column += "{}, ".format(k.strip())
        column = column[:-2]

        condition = ""
        for k in d_condition.split(","):
            condition += "{} = %s AND ".format(k.strip())
        
        condition = condition[:-5]
        
        self.conn.execute("SELECT {} FROM {} WHERE {}".format(column, table, condition), params)
        dados = self.conn.fetchall()
        if dados:
            table = dictUpdate["table"]
            d_column = dictUpdate["column_update"]
            d_condition = dictUpdate["condition"]
            params = dictUpdate["params_update"]

            column = ""
            for k in d_column.split(","):
                column += "{} = %s, ".format(k.strip())
            column = column[:-2]

            condition = ""
            for k in d_condition.split(","):
                condition += "{} = %s AND ".format(k.strip())
            
            condition = condition[:-5]
            
            self.conn.execute("UPDATE {} SET {} WHERE {}".format(table, column, condition), params)
        else:
            table = dictUpdate["table"]
            d_column = dictUpdate["column"]
            params = dictUpdate["params_insert"]

            column = ""
            for k in d_column.split(","):
                column += "`{}`, ".format(k.strip())
            column = column[:-2]

            condition = ""
            for k in d_column.split(","):
                condition += "%s, ".format(k.strip())

            condition = condition[:-2]

            self.conn.execute("INSERT {} ({}) VALUES ({})".format(table, column, condition), params)

        return self.conn.rowcount