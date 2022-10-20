from datetime import datetime
from re import A
from django.contrib.auth.models import User
import re
from auth_patients.models import Path_Patients, ViewDocsPatients
from auth_users.decorator import fetchHistoryPatient

# SALVAR DOCS PRINCIPAIS DOS PARCEIROS
def ApiPathDocsPatientsFunction(request):
    id = request.POST.get("id_user")
    type_doc = request.POST.get("type_doc")

    ObjetoPath = Path_Patients()
    ObjetoPath.id = id #Atribui valor para meu id
    ObjetoPath.etype = type_doc
    ObjetoPath.FILES = request.FILES

    ObjetoFunction = ObjetoPath.CreatePath()

    return {
        "response": True,
        "message": ObjetoFunction
    }

def ApiListDocsPatientsFunction(request):
    id = request.POST.get("id_user")

    ObjetoPath = ViewDocsPatients()
    ObjetoPath.id = id

    ObjetoFunction = ObjetoPath.VerificaPath()

    return {
        "response": True,
        "message": {
            "docs": ObjetoFunction,
            "history": fetchHistoryPatient(id)
        }
    }