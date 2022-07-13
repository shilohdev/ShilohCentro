from django.conf import settings
import os
import urllib.request
from auth_users.decorator import StartCollectionFunction
from functions.connection.models import CollectionScheduleDB, PatientsDB
from functions.general.decorator import json_with_success, json_without_success, dealStringify
from module_clicksign.models import ClickSignDB, ClickSignServices


def ModuleSendClickSignFunction(request):
    bodyData = request.GET
    if not bodyData.keys():
        return json_without_success("Nenhum parâmetro via get enviado.")

    id_coleta = bodyData.get('id', None)

    if not id_coleta:
        return json_without_success("Nenhum id de coleta enviado.")

    my_template_key = settings.CLICKSIGN_TEMPLATES_KEY.get(
        int(
            PatientsDB.objects.get(
                id_p=CollectionScheduleDB.objects.get(id=id_coleta).nome_p
            ).company_p
        )
    )
    print(id_coleta)
    print(my_template_key)
    
    StartCollectionFunction(id_coleta) # FAZ A ATUALIZAÇÃO DE STATUS

    ClickSignOBJ = ClickSignServices()
    return ClickSignOBJ.send(
       templateKey=my_template_key,
       id=bodyData.get('id'),
       name=bodyData.get('name'),
       email=bodyData.get('email'),
       phone=bodyData.get('phone'),
       data={
        "CONTRATANTE_RG": "53266655545",
        "CONTRATANTE_TELEFONE": "phone",
        # AQUI COLOCA TODOS OS PARAMETROS DO CONTRATO
       }
    )


def _get_path_by_doc_key(documentKey):
    # FUNCAO PARA PEGAR O PATH DO BANCO DE DADOS PELO DOCUMENT KEY
    path = ClickSignDB.objects.filter(
        document_key=documentKey
    ).last()

    if path:
        return path.document_path

    return None


def save_doc_clicksign(documentKey=None):
    import time
    #if not path:
    #    return json_without_success("Nenhum documento encontrado.")

    time.sleep(2)

    data, httpRequest = ClickSignServices().view(documentKey=documentKey)

    if httpRequest not in [200, 201]:
        return json_without_success("Nenhum documento encontrado.")

    signed_file_url = data.get('document', {}).get('downloads', {}).get('signed_file_url', None)
    if not signed_file_url:
        return json_without_success("Nenhum documento encontrado.")

    filename = "termo.pdf"
    p = ClickSignDB.objects.get(document_key=documentKey).document_path
    local_path = settings.BASE_DIR_DOCS + "/contracts" + p
    local_path_v = settings.BASE_DIR_DOCS + "/contracts" + p + "/"
    local_file =  f"{local_path_v}/{filename}"

    try:
        os.makedirs(local_path)
        os.makedirs(local_path_v)
    except OSError as ExceptionValue:
        print(ExceptionValue)

    print(signed_file_url)
    print(local_file)

    urllib.request.urlretrieve(signed_file_url, local_file)
    return True


def sign_document_by_doc_key(documentKey):
    ClickSignDB.objects.filter(
        document_key=documentKey
    ).update(
        status=1
    )

    return True


def saveContractClickSign(documentKey=None):
    # FUNCAO PARA ASSINAR O DOCUMENTO NO MYSQL
    sign_document_by_doc_key(documentKey)

    # FUNCAO PARA SALVAR O PDF NA MAQUINA VIRTUAL
    try:
        r = save_doc_clicksign(documentKey=documentKey)
        print(r)
    except Exception as ExceptionValue:
        print(ExceptionValue)

    return json_with_success("Documento salvo com sucesso.")


def WHookSendClickSignFunction(request):
    body = (request.body).decode()
    data = dealStringify(body)

    if not data:
        return json_without_success("Nenhum valor recebido.")

    event = data.get('event', {}).get('name')
    document_key = data.get('document', {}).get('key')

    print(event)
    if event == "auto_close":
        print(document_key)
        saveContractClickSign(documentKey=document_key)
        return json_with_success("Dados recebidos com sucesso.")

    return json_without_success("Nmnhum evento condizente com o cadastrado.")