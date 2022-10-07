from django.db import connections

from auth_finances.functions.solicitacoes.models import SolicitacaoReembolso


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



def CreatePermissionAll(request):
    with connections['auth_permissions'].cursor() as cursor:
 
        query = "SELECT id, perfil FROM auth_users.users where perfil LIKE 6"
        cursor.execute(query)
        dados = cursor.fetchall()
        if dados:
            print(dados)
            for id, perfil in dados:
                queryCreate = "INSERT INTO `auth_permissions`.`auth_permissions_allow` (`id_permission`, `id_user`, `nome_user`) VALUES ('21',  %s, '');"
                cursor.execute(queryCreate, (id,))

        return {
            "response": True,
            "message": "Acessos criados",
        }


def User_Information(request, status): #Função para pehar a info do usuario e usar como parametro
    with connections['auth_permissions'].cursor() as cursor:
        searchID = "SELECT DISTINCT a.perfil, a.id, a.nome, a.unity FROM auth_users.users a INNER JOIN admins.units_shiloh b ON a.unity = b.id_unit_s WHERE login LIKE %s "
        cursor.execute(searchID, (request.user.username,))
        dados = cursor.fetchall()
        if dados:
            for perfil, id_usuario, nome, unityY in dados:
                if status == "Pendente":
                    r = SolicitacaoReembolso.Solicitacao_Reembolso_Pendente_Function(perfil, unityY)
                    return r 
                if status == "Analise":
                    r = SolicitacaoReembolso.Solicitacao_Reembolso_Andamento_Function(perfil, unityY)
                    return r 
                if status == "Glosa":
                    r = SolicitacaoReembolso.Solicitacao_Reembolso_Glosa_Natingido_Function(perfil, unityY)
                    return r
                if status == "Finalizado":
                    r = SolicitacaoReembolso.Solicitacao_Reembolso_Finalizado_Function(perfil, unityY)
                    return r
                if status == "Juridico":
                    r = SolicitacaoReembolso.Solicitacao_Reembolso_Juridico_Function(perfil, unityY)
                    return r
                if status == "Dash_Pendente":
                    r = SolicitacaoReembolso.Dash_Solicitacao_Reembolso_Pendente(perfil, unityY)
                    return r
                if status == "Dash_Pago":
                    r = SolicitacaoReembolso.Dash_Solicitacao_Reembolso_Pago(perfil, unityY)
                    return r
                if status == "Dash_Andamento":
                    r = SolicitacaoReembolso.Dash_Solicitacao_Reembolso_Andamento(perfil, unityY)
                    return r
                if status == "Dash_Analise":
                    r = SolicitacaoReembolso.Dash_Solicitacao_Reembolso_Analise(perfil, unityY)
                    return r
                if status == "Dash_Glosa":
                    r = SolicitacaoReembolso.Dash_Solicitacao_Reembolso_Glosa(perfil, unityY)
                    return r
                if status == "Dash_Nao_Atingido":
                    r = SolicitacaoReembolso.Dash_Solicitacao_Reembolso_Nao_Atingido(perfil, unityY)
                    return r
                if status == "Dash_Total":
                    r = SolicitacaoReembolso.Qtd_Total_Solicitacoes_Reemboslo(perfil, unityY)
                    return r
        else:
            return {
                "response": "false",
                "message": "Login expirado, faça login novamente para continuar."
            }
