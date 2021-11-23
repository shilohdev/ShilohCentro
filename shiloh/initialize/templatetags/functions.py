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
def getPermissionUser(self):
    user = self
    with connections['authdb'].cursor() as cursor:
        #PERMISSÕES
        cursor.execute("SELECT name, email, phone, phone_aux, avatar FROM auth_users.users WHERE login LIKE %s LIMIT 1", (user,))
        dados = cursor.fetchall()
        if dados:
            for name, email, phone, phone_aux, avatar in dados:
                return {
                    "personal": {
                        "name": name,
                        "photo": avatar
                    },
                    "contacts": {
                        "email": email,
                        "phone": phone,
                        "phone_aux": phone_aux
                    }
                }

    return False