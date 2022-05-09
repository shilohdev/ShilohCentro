from django.db import connections
import numpy

def json_without_success(data):
    return {
        "response": False,
        "message": data
    }


def allowPermission(request, idPermission):
    login_usuario = request.user.username

    with connections['auth_permissions'].cursor() as cursor:
        params = (
            login_usuario,
            idPermission,
        )
        query = "SELECT ap_allow.id FROM auth_permissions.auth_permissions_allow ap_allow INNER JOIN auth_users.users u ON u.id = ap_allow.id_user INNER JOIN auth_permissions.permissions_id p_i ON p_i.id = ap_allow.id_permission WHERE u.login = %s AND p_i.id_description = %s"
        cursor.execute(query, params)
        dados = cursor.fetchall()

        return True if dados else False