from django.db import connections
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import ensure_csrf_cookie
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.http import JsonResponse
from django.contrib import messages
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from datetime import datetime
from auth_users.decorator import SearchModalExamsFunction, FunctionStartProcess, FunctionSearchTypeAnexo, FunctionStatus, searchConcluidosF, FunctionStatusSelect, FunctionStatusAgendaCancel, FunctionStatusAgendaFrustrar,ApiReagendarAgendaConcFunction, FunctionStatusAgendaConc, SearchModalScheduled, searchScheduledPickup, SearchSelectSchedule, ApiChangePatientsModalFunction,searchLead, SelectConvenio, ApiViewDataPatientsModalFunction, ApiCadastrePatienteFunction, searchLeads, searchIndication, searchUsers, ApiChangeUsersModalFunction, ApiViewDataPartnersModalFunction, ApiChangeStatusFunction, ApiViewDataUserModalFunction,TabelaPartners, searchPartiners, SearchUsersFull, DeleteConv, FScheduledPickup, searchService, searchDoctor, searchExame, FschedulePickup, CadastreUser, CadastrePartners, CadastreIndication, formatcpfcnpj, formatTEL, ApiChangeStatusConvenioFunction, cadastreConv, error, allowPage, searchTPerfil, searchCategoria, searchNurse, searchDriver, searchConvenio
from auth_finances.functions.exams.models import SearchMonthExamsConclFunction, searchrRefundCompletedFunction, FinalizeProcessFunction, SaveEditionsFinancesFunctions, FunctionModalFinances
import base64
import json
import time
from re import A
def csrf_failure(request, reason=""):
    raise PermissionDenied()


#CADASTRAR USUARIO
@login_required
def cadastreUserViews(request):
    if allowPage(request, "register_user") == False:
        return error(request)
    searchPerfil = searchTPerfil(request)
    return render(request, 'manage/cadastre/Perfis/cadastreUser.html', {"arr_SearchPerfil": searchPerfil})

    
#CADASTRAR PARCEIROS
@login_required
def cadastrePartnesViews(request):
    SsearchCategoria = searchCategoria(request)
    return render(request, 'manage/cadastre/Perfis/cadastrePartnes.html', {"arr_SearchCategoria": SsearchCategoria})


#API CADASTRAR USUARIOS
def ApiCadastreUser(request):
    array = CadastreUser(request)
    return JsonResponse(array, safe=False, status=200)

#API CADASTRAR PARCEIROS
def ApiCadastrePartners(request):
    array = CadastrePartners(request)
    return JsonResponse(array, safe=False, status=200)


#CADASTRAR INDICAÇÃO
@login_required
def cadastreIndicationViews(request):
    sSelect_conv =  SelectConvenio(request)
    return render(request, 'manage/cadastre/Perfis/cadastreIndication.html', {"arr_SelectConvenio": sSelect_conv})

    
#API CADASTRAR INDICAÇÃO
def ApiCadastreIndication(request):
    array = CadastreIndication(request)
    return JsonResponse(array, safe=False, status=200)


#API FORMATAR CPF
def apiFormatCPF(request):
    array = formatcpfcnpj(request)
    return JsonResponse(array, safe=False, status=200)

     
#API FORMATAR NÚMERO DE TEL
def apiFormatTEL(request):
    array = formatTEL(request)
    return JsonResponse(array, safe=False, status=200)


#CADASTRAR CONVENIO
@login_required
def cadastreConvenioViews(request):
    if allowPage(request, "register_convenio") == False:
        return error(request)
    SsearchConvenio =  searchConvenio(request)
    return render(request, 'manage/cadastre/Convenio/cadastreConvenio.html', {"arr_SearchConvenio": SsearchConvenio,})

    
#API CADASTRAR CONVENIO
def ApiCadastreConvenio(request):
    array =  cadastreConv(request)
    return JsonResponse(array, safe=False, status=200)

def ApiChangeStatusConvenio(request):
    array =  ApiChangeStatusConvenioFunction(request)
    return JsonResponse(array, safe=False, status=200)


#API PERMISSOES USERS
def ApiPermissionsUsers(request):
    array =  allowPage(request, "")
    return JsonResponse(array, safe=False, status=200)

    
#AGENDAR COLETA
@login_required
def schedulePickupViews(request):
    SsearchNurse =  searchNurse(request)
    SsearchDriver =  searchDriver(request)
    sSelect_conv =  SelectConvenio(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchPacienteSe = SearchSelectSchedule(request)
    return render(request, 'manage/agenda/schedulePickup.html', {"arr_SearchNurse": SsearchNurse, "arr_SearchService": SsearchService, "arr_SearchDriver": SsearchDriver, "arr_SelectConvenio": sSelect_conv, "arr_SearchExame": SsearchExame, "arr_SearchPacienteSe": SsearchPacienteSe})

#API AGENDAR COLETA
def ApiSchedulePickupViews(request):
    array =  FschedulePickup(request)
    return JsonResponse(array, safe=False, status=200)
    
#CONSULTAR COLETA AGENDADA
@login_required
def ScheduledPickupViews(request):
    SsearchDoctor = searchDoctor(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchNurse =  searchNurse(request)
    SsearchDriver =  searchDriver(request)
    SsearchConvenio =  searchConvenio(request)
    SsearchScheduledPickup =  searchScheduledPickup(request)
    SsearchColors =  ApiScheduledPickupModalViews(request)
    SsearchStatus =  FunctionStatusSelect(request)
    return render(request, 'manage/agenda/ScheduledPickup.html',  {"arr_SearchDoctor": SsearchDoctor, "arr_SearchExame": SsearchExame, "arr_SearchService": SsearchService, "arr_SearchNurse": SsearchNurse, "arr_SearchDriver": SsearchDriver, "arr_SearConvenio": SsearchConvenio, "arr_SearchScheduledPickup": SsearchScheduledPickup,  "arr_SearchColor": SsearchColors, "arr_SearchStatus": SsearchStatus,})


#API CONSULTAR COLETA
def ApiScheduledPickupViews(request):
    array = FScheduledPickup(request)
    return JsonResponse(array, safe=False, status=200)

#API DELETAR CONVENIO
def DeleteConvenio(request):
    array =  DeleteConv(request)
    return JsonResponse(array, safe=False, status=200)
 

#LISTAR USUARIOS
@login_required
def listUsersViews(request):
    if allowPage(request, "list_users") == False:
        return error(request)
    searchPerfil = searchTPerfil(request)
    arrSearchUsersFull = SearchUsersFull(request)
    return render(request, 'manage/listers/users/listUsers.html', { "arr_SearchPerfil": searchPerfil, "arr_SearchUsersFull": arrSearchUsersFull })


#API LISTAR USUARIOS
def ApiListUsersViews(request):
    array = searchUsers(request)
    return JsonResponse(array, safe=False, status=200)

#MODAL USUARIO
def ApiViewDataUserModal(request):
    array = ApiViewDataUserModalFunction(request)
    return JsonResponse(array, safe=False, status=200)


def ApiChangeStatus(request):
    array = ApiChangeStatusFunction(request)
    return JsonResponse(array, safe=False, status=200)


#MODAL ATUALIZAR USUARIOS
@ensure_csrf_cookie
def ApiChangeUsersModal(request):
    array = ApiChangeUsersModalFunction(request)
    return JsonResponse(array, safe=False, status=200)


#LISTAR PARCEIROS
@login_required
def listPartnesViews(request):
    if allowPage(request, "list_partners") == False:
        return error(request)

    SsearchCategoria = searchCategoria(request)
    SsearchPartiners = TabelaPartners(request)
    return render(request, 'manage/listers/partners/listPartners.html', {"arr_SearchCategoria": SsearchCategoria, "arr_SearchPartiners": SsearchPartiners})


#API LISTAR PARCEIROS
@ensure_csrf_cookie
def ApiListPartnesViews(request):
    array = searchPartiners(request)
    return JsonResponse(array, safe=False, status=200)


#MODAL PARCEIROS
@ensure_csrf_cookie #<<<< requisitar a chave do token
def ApiViewDataPartnersModal(request):
    array = ApiViewDataPartnersModalFunction(request)
    return JsonResponse(array, safe=False, status=200)


#LISTAR PACIENTES > INDICAÇÃO
@login_required
def listIndicationViews(request):
    if allowPage(request, "list_indication") == False:
        return error(request)

    SsearchIndication = searchIndication(request)
    SsearchConvenio =  searchConvenio(request)
    return render(request, 'manage/listers/indication/listIndication.html', {"arr_SearchIndication": SsearchIndication, "arr_SearchConvenio": SsearchConvenio,})



#LISTAR LEADS
@login_required
def listLeadsViews(request):
    if allowPage(request, "list_lead") == False:
        return error(request)
    SsearchLeads = searchLead(request)
    return render(request, 'manage/listers/lead/listLead.html', {"arr_SearchLeads": SsearchLeads, })


#LISTAR PACIENTES SEARCH
@login_required
def CadastrePatientViews(request):
    if allowPage(request, "cadastre_patients") == False:
        return error(request)
    SsearchPatients = searchLeads(request)
    SsearchConvenio =  searchConvenio(request)
    return render(request, 'manage/cadastre/Perfis/cadastrePatient.html', {"arr_SearchPatients": SsearchPatients,"arr_SearchConvenio": SsearchConvenio, })
    
    
#CADASTRAR PACIENTES
def ApiCadastrePatientViews(request):
    array = ApiCadastrePatienteFunction(request)
    return JsonResponse(array, safe=False, status=200)
 

#MODAL PACIENTES
def ApiViewDataPatientsModal(request):
    array = ApiViewDataPatientsModalFunction(request)
    return JsonResponse(array, safe=False, status=200)


#MODAL PACIENTES UPDATE
def ApiChangePatientsModal(request):
    array = ApiChangePatientsModalFunction(request)
    return JsonResponse(array, safe=False, status=200)

def ApiScheduledPickupModalViews(request):
    array = SearchModalScheduled(request)
    return JsonResponse(array, safe=False, status=200)

# API STATUS CONCLUIDO
def ApiStatusAgendaConc(request):
    array = FunctionStatusAgendaConc(request)
    return JsonResponse(array, safe=False, status=200)


def ApiReagendarAgendaConc(request):
    array = ApiReagendarAgendaConcFunction(request)
    return JsonResponse(array, safe=False, status=200)

    
# API STATUS FRUSTRAR
def ApiStatusAgendaFrustrado(request):
    array = FunctionStatusAgendaFrustrar(request)
    return JsonResponse(array, safe=False, status=200)
    
# API STATUS CANCELAR
def ApiStatusAgendaCancel(request):
    array = FunctionStatusAgendaCancel(request)
    return JsonResponse(array, safe=False, status=200)


#FINANCEIRO
#@login_required
def FinancialExamsViews(request):
    #if allowPage(request, "finances_exams") == False:
        #return error(request)
    SearchCompletedExams =  searchConcluidosF(request)
    SearchStratusProgress = FunctionStatus(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)
    return render(request, 'finances/exams/exams-concl.html', {"arr_SearchCompletedExams": SearchCompletedExams, "arr_SearchStratusProgress": SearchStratusProgress, "arr_SearchTypeAnexo": SearchTypeAnexo, })

# MODAL FINANCES
def SearchModalExams(request):
    array = SearchModalExamsFunction(request)
    return JsonResponse(array, safe=False, status=200)


# API INCIAIR PROCESSO
def ApiStartProcess(request):
    array = FunctionStartProcess(request)
    return JsonResponse(array, safe=False, status=200)


# API MODAL
def SearchModalExamsFinances(request):
    array = FunctionModalFinances(request)
    return JsonResponse(array, safe=False, status=200)


#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
def SaveEditionsFinances(request):
    array = SaveEditionsFinancesFunctions(request)
    return JsonResponse(array, safe=False, status=200)


#FINALIZAR PROCESSO MODAL FINANCEIRO EXAME
def ApiFinalizeProcess(request):
    array = FinalizeProcessFunction(request)
    return JsonResponse(array, safe=False, status=200)


def SearchMonthExamsConcl(request):
    array = SearchMonthExamsConclFunction(request)
    return JsonResponse(array, safe=False, status=200)


def RefundCompletedViews(request):
    #if allowPage(request, "nome da pagina") == False:
        #return error(request)
    SearchRefundCompleted = searchrRefundCompletedFunction(request)
    return render(request, 'finances/exams/refund-completed.html',  {"arr_SearchRefundCompleted": SearchRefundCompleted,})
