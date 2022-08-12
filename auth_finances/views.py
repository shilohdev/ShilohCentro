from itertools import count
import json
from re import A
from struct import error
from tracemalloc import start
from django.shortcuts import get_object_or_404, render
from requests import request
from auth_permissions.decorator import User_Information
from auth_users.decorator import FilePhotoViewFunction, FunctionSearchTypeAnexo, FunctionStatus, allowPage
from django.http import HttpResponse
import time
from django.contrib.auth.decorators import login_required
from auth_users.models import Users



def teste(request):
    start_time = time.time()

    a= Users.objects.exclude(status='Cancelado')
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

    ViewFoto = FilePhotoViewFunction(request)
    SearchStratusProgress = FunctionStatus(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)

    Solicitacao_Pendente =  User_Information(request, 'Pendente')
    Solicitacao_Andamento_Pendente = User_Information(request, 'Analise')
    Solicitacao_Glosa_Natingido = User_Information(request, 'Glosa')
    Solicitacao_Finalizada = User_Information(request, 'Finalizado')
    Dash_reemsolso_pendente = User_Information(request, 'Dash_Pendente')
    Dash_reemsolso_pago = User_Information(request, 'Dash_Pago')
    Dash_reembolso_andamento = User_Information(request, 'Dash_Andamento')
    Dash_reembolso_analise = User_Information(request, 'Dash_Analise')
    Dash_reembolso_glosa = User_Information(request, 'Dash_Glosa')
    Dash_reembolso_nao_atingido = User_Information(request, 'Dash_Nao_Atingido')
    Dash_reembolso_total = User_Information(request, 'Dash_Total')

    return render(request, 'finances/exams/request-refund.html', 
    {
        "arr_ViewFoto": ViewFoto,
        "arr_SearchTypeAnexo": SearchTypeAnexo, 
        "arr_SearchStratusProgress": SearchStratusProgress,
        
        "arr_Solicitacao_Reembolso_Pendente": Solicitacao_Pendente,
        "arr_Solicitacao_Andamento_Pendente": Solicitacao_Andamento_Pendente,
        "arr_Solicitacao_Glosa_Natingido": Solicitacao_Glosa_Natingido,
        "arr_Solicitacao_Finalizada": Solicitacao_Finalizada,
        "arr_Dash_reemsolso_pendente": Dash_reemsolso_pendente,
        "arr_Dash_reemsolso_pago": Dash_reemsolso_pago,
        "arr_Dash_reembolso_andamento": Dash_reembolso_andamento,
        "arr_Dash_reembolso_analise": Dash_reembolso_analise,
        "arr_Dash_reemsolso_glosa": Dash_reembolso_glosa,
        "arr_Dash_reemsolso_nao_atingido": Dash_reembolso_nao_atingido,
        "arr_Dash_reembolso_total": Dash_reembolso_total,
    
    })

