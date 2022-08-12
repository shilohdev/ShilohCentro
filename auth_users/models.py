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