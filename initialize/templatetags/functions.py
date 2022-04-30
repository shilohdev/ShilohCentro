from django import template
from datetime import datetime
from datetime import timedelta
from django.db import connections
import json
import re
import base64
import hashlib

register = template.Library()

@register.simple_tag
def define(val=None):
    return val


@register.filter
def replace_espace(self):
    return self.replace(' ','_')


@register.filter
def convertTitle(self):
    if self != None and self != "":
        strlower = self.lower()
        return strlower[0].upper() + strlower[1:]
    else:
        return self


@register.filter
def allDataUser(self):
    arr_response = []
    user = str(self)
    if user in ["", None]:
        return None

    with connections['auth_users'].cursor() as cursor:
        query = f"SELECT p_i.id, p_i.id_description FROM auth_permissions.auth_permissions_allow p INNER JOIN auth_users.users u ON u.id = p.id_user INNER JOIN auth_permissions.permissions_id p_i ON p_i.id = p.id_permission WHERE u.login LIKE '{user}'"
        cursor.execute(query)
        dados = cursor.fetchall()
        if dados:
            for p_id, p_id_d in dados:
                arr_response.append(p_id_d)
    
    return arr_response


@register.filter
def fetchUser(self):
    user = self
    with connections['auth_users'].cursor() as cursor:
        query = "SELECT id, substring_index(nome, ' ', 3) as NomeLog from auth_users.users WHERE login LIKE %s"
    
        cursor.execute(query, (user,))
        dados = cursor.fetchall()
        if dados:
            for id, nome in dados:
                return {
                    #"id": id,
                    "nome": nome
                }
    return {}