from django.db import models
from enum import Enum


class BancoDeDados(str, Enum):
    DB = 'auth_finances'
    DBA = 'admins'
    DBCLICKSIGN = 'clicksigndb'
    DBCOLLECTION = 'auth_agenda'
    DBCUSTOMERREFER = 'customer_refer'
    DB_USER = 'auth_users'


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


class DBClickSign(models.Model):
    use_db = BancoDeDados.DBCLICKSIGN.value
    objects = DbManager()

    class Meta:
        abstract = True


class DBCollection(models.Model):
    use_db = BancoDeDados.DBCOLLECTION.value
    objects = DbManager()

    class Meta:
        abstract = True


class DBCustomerRefer(models.Model):
    use_db = BancoDeDados.DBCUSTOMERREFER.value
    objects = DbManager()

    class Meta:
        abstract = True





class DBusers(models.Model):
    use_db = BancoDeDados.DB_USER.value
    objects = DbManager()

    class Meta:
        abstract = True