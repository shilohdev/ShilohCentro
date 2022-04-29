from django.db import models
from enum import Enum


class BancoDeDados(str, Enum):
    DB = 'auth_finances'
    DBA = 'admins'


class DbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()

        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, 'use_db'):
            qs = qs.using(self.model.use_db)

        return qs


class DB(models.Model):
    use_db = BancoDeDados.DB.value
    objects = DbManager()

    class Meta:
        abstract = True


class DBAdmins(models.Model):
    use_db = BancoDeDados.DBA.value
    objects = DbManager()

    class Meta:
        abstract = True