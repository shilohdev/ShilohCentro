from functions.connection.models import Connection
import json


def fetchPermissions():
    dict_response = {}

    db = Connection('userdb', '', '', '', '')
    db.table = "auth_permissions.permissions_id p_i INNER JOIN auth_permissions.permissions_type p_t ON p_i.type_category = p_t.id"
    dados = db.fetch(["p_i.id, p_i.id_description, p_i.description, p_t.id, p_t.descriptions"], False)
    if dados:
        for id_pk, id_permission, description_permission, id_category, description_category in dados:
            id_category = str(id_category)
            id_permission = str(id_permission)
            if id_category not in dict_response:
                dict_response[id_category] = {
                    "name": description_category,
                    "data": []
                }
            
            category_data = dict_response[id_category]["data"]
            category_data.append({
                "category": id_category,
                "id_pk": id_pk,
                "id": id_permission,
                "name": description_permission
            })
    
    return dict_response


def fetchUserPermissions(user_id):
    arr_response = []

    db = Connection('userdb', '', '', '', '')
    db.table = "auth_permissions.auth_permissions_allow p_allow"
    db.condition = "WHERE p_allow.id_user = %s"
    db.params = (user_id,)
    dados = db.fetch(["p_allow.id_permission, p_allow.id_user"], True)
    if dados:
        for id_permission, id_user in dados:
            arr_response.append(id_permission)
    
    return arr_response


def savePermissionsFunction(request):
    user = request.POST.get('id_user')
    permissions = request.POST.get('permissions')
    try:
        permissions = json.loads(permissions)
    except:
        return {
            "response": "false",
            "message": "Não foi encontrada nenhuma permissão."
        }

    
    db = Connection('userdb', '', '', '', '')
    cursor = db.connection()

    # DELETE PERMISSIONS
    params = (
        user,
        
    )
    cursor.execute("DELETE FROM auth_permissions.auth_permissions_allow WHERE id_user = %s", params)

    # INSERT PERMISSIONS
    queryP = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id_permission`, `id_user`, `nome_user`) VALUES (%s, %s, %s)"
    for id_permission in permissions:
        params = (
            id_permission,
            user,
            "",
        )
        cursor.execute(queryP, params)

    return {
        "response": "true",
        "message": "Permissões salvas com sucesso!"
    }