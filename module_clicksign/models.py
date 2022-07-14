from datetime import datetime
from functions.general.decorator import ExcludeCaractersByArray, json_with_success, json_without_success
from django.conf import settings
import json, urllib, requests
from django.db import models
from functions.connection.db import DBClickSign


class ClickSignDB(DBClickSign):
    id = models.AutoField("ID", primary_key=True, auto_created=True)
    document_key = models.CharField("Document Key", max_length=350, null=True, blank=True, default=None)
    document_path = models.CharField("Document Key", max_length=150, null=True, blank=True, default=None)
    document_name = models.CharField("Document Key", max_length=75, null=True, blank=True, default=None)
    status = models.BooleanField(default=False)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    coleta_id = models.IntegerField(default=None)
    
    class Meta:
        db_table = "registros_documents"
        indexes = [
            models.Index(fields=[
                "coleta_id",
            ])
        ]


class ClickSignServices:
    def __init__(self) -> None:
        self.sandbox = settings.CLICKSIGN_DEBUG
        self.standard_send_message = settings.CLICKSIGN_SEND_MESSAGE if not bool(self.sandbox) else settings.CLICKSIGN_SANDBOX_SEND_MESSAGE
        self.url = settings.CLICKSIGN_URL if not bool(self.sandbox) else settings.CLICKSIGN_SANDBOX_URL
        self.token = settings.CLICKSIGN_TOKEN if not bool(self.sandbox) else settings.CLICKSIGN_SANDBOX_TOKEN
        self.headers = {
            'Host': 'app.clicksign.com',
            'content-type': 'application/json',
            'Accept': 'application/json'
        }

    def _connect_ex(self):
        return urllib.parse.urlencode({
            "access_token": self.token
        })

    def create_signature(self, name=None, email=None, phone=None, documentation=None, birthday=None, has_documentation=False, delivery='email'):
        payload_qs = self._connect_ex()
        domain_url = self.url + "/api/v1/signers?{}".format(payload_qs)

        payload = {
            "signer": {
                "email": email,
                "phone_number": ExcludeCaractersByArray(phone, ["(", ")", "-", " ", ".", "/", "+"]),
                "auths": ["email"],
                "name": name,
                #"documentation": "123.321.123-40",
                #"birthday": "1983-03-31",
                "delivery": delivery,
                "has_documentation": has_documentation,
                "selfie_enabled": False,
                "handwritten_enabled": False,
                "official_document_enabled": False,
                "liveness_enabled": False,
                "facial_biometrics_enabled": False
            }
        }
        r = requests.post(domain_url, data = json.dumps(payload), headers=self.headers)
    
        if r.status_code in [200, 201]:
            return r.json(), 200

        try:
            data = r.json()
        except Exception as ExceptionValue:
            print("Error clicksign: {}".format(ExceptionValue))
            data = json.dumps(r.text)
        
        return data, 500
    
    def create_document(self, templateKey=None, data=None, path=None):
        if not templateKey:
            return json_without_success("Nenhum documento enviado.")

        payload_qs = self._connect_ex()
        domain_url = self.url + "/api/v1/templates/{}/documents?{}".format(templateKey, payload_qs)

        payload = {
            "document": {
                "path": path,
                "template": {
                    "data": data
                }
            }
        }

        r = requests.post(domain_url, data = json.dumps(payload), headers=self.headers)
        if r.status_code in [200, 201]:
            return r.json(), 200

        try:
            data = r.json()
        except Exception as ExceptionValue:
            print("Error clicksign: {}".format(ExceptionValue))
            data = json.dumps(r.text)
        
        return data, 500
    
    def _add_signature_to_document(self, documentKey=None, signatureKey=None):
        if not signatureKey:
            return json_without_success("Nenhum assinante encontrado.")

        payload_qs = self._connect_ex()
        domain_url = self.url + "/api/v1/lists?{}".format(payload_qs)

        payload = {
            "list": {
                "document_key": documentKey,
                "signer_key": signatureKey,
                "sign_as": "sign"
            }
        }

        r = requests.post(domain_url, data = json.dumps(payload), headers=self.headers)
        if r.status_code in [200, 201]:
            return r.json(), 200

        try:
            data = r.json()
        except Exception as ExceptionValue:
            print("Error clicksign: {}".format(ExceptionValue))
            data = json.dumps(r.text)
        
        return data, 500
    
    def _notify_signature(self, requestSignatureKey=None):
        if not requestSignatureKey:
            return json_without_success("Signatário não encontrado.")

        payload_qs = self._connect_ex()
        domain_url = self.url + "/api/v1/notifications?{}".format(payload_qs)

        payload = {
            "request_signature_key": requestSignatureKey,
            "message": self.standard_send_message
        }

        r = requests.post(domain_url, data = json.dumps(payload), headers=self.headers)
        if r.status_code in [200, 201]:
            return r.json(), 200

        try:
            data = r.json()
        except Exception as ExceptionValue:
            data = json.dumps(r.text)
        
        return data, 500
    
    def view(self, documentKey=None):
        if not documentKey:
            return json_without_success("Documento não encontrado.")

        payload_qs = self._connect_ex()
        domain_url = self.url + "/api/v1/documents/{}?{}".format(documentKey, payload_qs)

        payload = {}

        r = requests.get(domain_url, data = payload, headers=self.headers)
        if r.status_code in [200, 201]:
            return r.json(), 200

        try:
            data = r.json()
        except Exception as ExceptionValue:
            data = json.dumps(r.text)
        
        return data, 500
    
    def cancel(self, documentKey=None):
        if not documentKey:
            return json_without_success("Documento não encontrado.")

        payload_qs = self._connect_ex()
        domain_url = self.url + "/api/v1/documents/{}/cancel?{}".format(documentKey, payload_qs)

        payload = {}

        alternate_headers = {
            "Host": "sandbox.clicksign.com",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        r = requests.patch(domain_url, data = json.dumps(payload), headers=alternate_headers)
        if r.status_code in [200, 201]:
            return r.json(), 200

        try:
            data = r.json()
        except Exception as ExceptionValue:
            data = json.dumps(r.text)
        
        return data, 500

    def save_document_in_db(self, coletaId=None, documentKey=None, fileName=None, path=None):
        if documentKey and path in ["", None]:
            return False
        
        if not ClickSignDB.objects.filter(document_key=documentKey).last():
            ClickSignDB.objects.create(
                document_key=documentKey,
                document_name=fileName,
                document_path=path,
                status=0,
                coleta_id=coletaId
            )
    
    def cancel_document_by_id(self, id=None):
        if not id:
            return False
        
        data = ClickSignDB.objects.filter(coleta_id=id).all()
        for key in data:
            document_key = key.document_key
            try:
                self.cancel(documentKey=document_key)
            except Exception as ExceptionValue:
                continue
        
        return True

    def send(self, templateKey=None, id=None, name=None, email=None, phone=None, data=None):
        data = data if data else {}

        createSignature, httpRequest = self.create_signature(name=name, email=email, phone=phone)
        if httpRequest not in [200, 201]:
            return json_without_success("[1] Não foi possível criar um assinante para o documento.")

        signer_key = createSignature.get('signer', {}).get('key')
        if not signer_key:
            return json_without_success("[2] Não foi possível criar um assinante para o documento.")

        id = str(id)

        self.cancel_document_by_id(id=id)

        dateNow = str(datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
        path_signer_folder = f"/{name}/{dateNow}"
        path_signer = f"/{id}/{name}/{dateNow}/Termo_de_Coleta.docx"

        document_key, httpRequest = self.create_document(templateKey=templateKey, data=data, path=path_signer)
        if httpRequest not in [200, 201]:
            return json_without_success("[3] Não foi possível criar um documento.")

        document_key = document_key.get('document', {}).get('key')
        if not document_key:
            return json_without_success("Não foi possível criar o documento.")

        append_signer_to_doc, httpRequest = self._add_signature_to_document(documentKey=document_key, signatureKey=signer_key)

        request_signature_key = append_signer_to_doc.get('list', {}).get('request_signature_key', {})
        if request_signature_key in ["", None]:
            return json_without_success("Nenhum signatário encontrado.")
        
        notify, httpRequest = self._notify_signature(requestSignatureKey=request_signature_key)

        self.save_document_in_db(coletaId=id, documentKey=document_key, path=path_signer_folder)

        return json_with_success("Documento enviado com sucesso.")