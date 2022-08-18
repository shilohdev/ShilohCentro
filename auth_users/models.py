from django.db import connections
from django.db import models
from functions.connection.db import DBusers



class Users(DBusers):
    id = models.AutoField(primary_key=True, auto_created=True)
    nome = models.CharField(max_length=255, null=True, blank=True, default=None)
    status = models.CharField(max_length=45, null=True, blank=True, default=None)
    perfil = models.CharField(max_length=255, null=True, blank=True, default=None)
    data_regis = models.DateField(null=True, blank=True, default=None)

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=[
                "id",
            ])
        ]

    def __str__(self):
        return self.nome




class HistoryPartners:
    def __init__(self, id=None) -> None: 
        self.id = id

    def localizaHistorico(self):
        with connections['auth_users'].cursor() as cursor:
            query = "SELECT r.id, u.nome, r.id_parceiro, r.tp_operacao, r.descricao, r.data_registro FROM auth_users.register_partners r INNER JOIN auth_users.users u ON r.id_parceiro = u.id WHERE r.id_parceiro = {}".format(self)
            cursor.execute(query)
            dados = cursor.fetchall()

            if not dados:
                return []

            return [{
                "id": id,
                "nome": nome,
                "id_parceiro": id_parceiro,
                "acao": tp_operacao,
                "descricao": descricao,
                "data": data_registro
            } for id, nome, id_parceiro, tp_operacao, descricao, data_registro in dados]
            