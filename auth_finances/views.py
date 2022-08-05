from itertools import count
import json
from re import A
from struct import error
from tracemalloc import start
from django.shortcuts import get_object_or_404, render
from requests import request
from auth_finances.functions.solicitacoes.models import Solicitacao_Reembolso_Pendente_Function
from auth_permissions.decorator import User_Information
from auth_users.decorator import allowPage
from functions.connection.models import Partnerss
from django.http import HttpResponse
import time
from django.contrib.auth.decorators import login_required



def teste(request):
    start_time = time.time()

    a= Partnerss.objects.exclude(status='Cancelado')
    print(a)
    end_time = time.time()
    duration = start_time - end_time
    print("durou média de: ", duration )
    return HttpResponse(a)


#FINANCEIRO
@login_required
#SOLICITAÇÃO DE REEMBOLSO
def ReembolsoFinanceiro(request):
    if allowPage(request, "agend_concluidos") == False:
        return error(request)
    
    Solicitacao_Pendente =  User_Information(request, 'Pendente')
    Solicitacao_Andamento_Pendente = User_Information(request, 'Analise')

    return render(request, 'finances/exams/exams-concl.html', 
    {
        "arr_Solicitacao_Reembolso_Pendente": Solicitacao_Pendente,
        "arr_Solicitacao_Andamento_Pendente": Solicitacao_Andamento_Pendente,
    })

