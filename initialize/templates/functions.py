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
    dict_response = {
        "name": None,
        "pages": [],
        "titles": []
    }
    with connections['auth_users'].cursor() as cursor:
        #PERMISSÕES 
        cursor.execute("SELECT p.id_permission, p.id_user, pg.description, pg.redirect_url, pg.icon, pt.description, pm.description, pm.icon FROM auth_permissions.auth_permissions_allow p INNER JOIN auth_users.users u ON u.id = p.id_user INNER JOIN auth_permissions.permission_page pg ON pg.permission_id = p.id_permission INNER JOIN auth_permissions.permission_page_module pm ON pm.id = pg.module INNER JOIN auth_permissions.permission_type_page pt ON pt.id = pm.id_permission_type WHERE u.login LIKE %s", (self,))
        dados = cursor.fetchall()
        if dados:
            titles_response = []
            molde_response = {}
            for id_permission, id_user, pg_description, pg_redirect_url, pg_icon, pt_title, pm_description, pm_icon in dados:
                if pt_title not in molde_response:
                    molde_response[pt_title] = {}
                
                if pm_description not in molde_response[pt_title]:
                    molde_response[pt_title][pm_description] = {
                        "icon": pm_icon,
                        "pages": []
                    }
                
                pages_response = molde_response[pt_title][pm_description]["pages"]
                pages_response.append({
                    "description": pg_description,
                    "url": pg_redirect_url,
                    "icon": pg_icon
                })
                if pt_title not in [titles_response]:
                    titles_response.append(pt_title)
            
            dict_response.update({
                "pages": molde_response,
                "titles": titles_response
            })

    arr = []
    for key in dict_response["pages"]:
        p = {
            "description": key,
            "icon": "",
            "pages": []
        }
        for j in dict_response["pages"][key]:
            n = {
                "description": j,
                "icon": dict_response["pages"][key][j]["icon"],
                "pages": []
            }
            for ee in dict_response["pages"][key][j]["pages"]:
                n["pages"].append({
                    "description": ee["description"],
                    "url": ee["url"],
                    "icon": ee["icon"],
                })

            p["pages"].append(n)
        
        arr.append(p)
    
    return arr