from functions.connection.models import Connection
from functions.permissions.decorator import fetchUserPermissions

def fetchUsers():
    arr_response = []

    db = Connection('userdb', '', '', '', '')
    db.table = "auth_users.users u"
    dados = db.fetch(["u.id, u.nome, u.data_nasc, u.email, u.tel1, u.tel2, u.cep, u.rua, u.numero, u.bairro, u.city, u.uf"], False)
    if dados:
        for id_user, name, birthday_user, email, tel1, tel2, cep, rua, numero, bairro, city, uf in dados:
            permissions = fetchUserPermissions(id_user)
            arr_response.append({
                "id": str(id_user),
                "category": "",
                "personal": {
                    "name": name,
                    "birthday": birthday_user
                },
                "contacts": {
                    "email": email,
                    "main_phone": tel1,
                    "aux_phone": tel2
                },
                "address": {
                    "zipcode": cep,
                    "street": rua,
                    "number": numero,
                    "district": bairro,
                    "city": city,
                    "state": uf
                },
                "permissions": str(permissions)
            })
    
    return arr_response