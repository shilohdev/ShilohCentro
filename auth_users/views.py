from django.views import View
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
from auth_users.decorator import errors, ApiViewDataPartnersModalFunctionINT, ModalExamsFinanceFileRemoveFunctionInt, SearchStatusLeadFilterFunction, FunctionSearchStatusLead, StatusNegative, iInfoLog, IniciarColetaFunction, searchRouteNurse, searchUnidadeTabela, RetfundFFinalizado, RetfundFConcl, SearchMonthIntFunction, FunctionStatusAgendaConcInt, SearchModalScheduledInt, searchScheduledPickupInt, FschedulePickupInt, SearchSelectInterno, CountAgendamentAtrasadosFunction, CountAgendamentsCFunction, CountAgendamentsCSFunction, CountAgendamentsFFunction, CountAgendamentsPFunction,  CountLeadsDayFunction, CountLeadsMesFunction, CountLeadsFunction, SaveEditionsPatientFunction, searchUnit, ApiChangeStatusUnitFunction, cadastreUnit, UpdatePerfil, CadastreLead, searchDoctorLead, SearchLeadsAll, searchIndicationUnit, TabelaPartnersUnit, searchPatientsUnit, ModalExamsFinanceFileRemoveFunction, SearchModalExamsFunction, FunctionStartProcess, FunctionSearchTypeAnexo, FunctionStatus, searchConcluidosF, FunctionStatusSelect, FunctionStatusAgendaCancel, FunctionStatusAgendaFrustrar,ApiReagendarAgendaConcFunction, FunctionStatusAgendaConc, SearchModalScheduled, searchScheduledPickup, SearchSelectSchedule, DeletePatientsFilesFunction, FetchPatientsFilesFunction, ApiChangePatientsModalFunction,searchLead, SelectConvenio, ApiViewDataPatientsModalFunction, ApiCadastrePatienteFunction, searchLeads, searchIndication, searchUsers, ApiChangeUsersModalFunction, ApiViewDataPartnersModalFunction, ApiChangeStatusFunction, ApiViewDataUserModalFunction,TabelaPartners, searchPartiners, SearchUsersFull, DeleteConv, FScheduledPickup, searchService, searchDoctor, searchExame, FschedulePickup, CadastreUser, CadastrePartners, CadastreIndication, formatcpfcnpj, formatTEL, ApiChangeStatusConvenioFunction, cadastreConv, error, allowPage, searchTPerfil, searchCategoria, searchNurse, searchDriver, searchConvenio
from auth_finances.functions.exams.models import valTotalCommercialFunction, valTotalPartinersF, ClosingUnitResult, ClosingUnitAnalise, SearchFinanceIntGlosa, SearchFinanceIntAgendado, SearchFinanceInt, TableClosingIntFilter, TableClosingInt, SaveAnexoFunction, payCommercialFunction, SearchInfoCommercialFunction, searchNotAtingeClosingCommercial, FilterMonthClosingCommercial, TableClosingCommercial, SearchInfoFunction, payPartnersVFunction, searchNotAtingeClosingPartners, FilterMonthClosingPartners, TableClosingPartners, SearchMonthExamsRefundF, SearchMonthSolicitation, pesqMesInternoFinalizados, searchGlosses, FunctionStatusN, searchNotReached, SearchMonthExamsConclFunction, searchrRefundCompletedFunction, FinalizeProcessFunction, SaveEditionsFinancesFunctions, FunctionModalFinances
from functions.general.decorator import BodyDecode
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
    searchUnity = searchUnit(request)
    return render(request, 'manage/cadastre/Perfis/cadastreUser.html', {"arr_SearchPerfil": searchPerfil,  "arr_SearchUnit": searchUnity})

    
#ATUALIZAR USUARIO INTERNO
@login_required
def ApiUpdatePerfil(request):
    if allowPage(request, "register_user") == False:
        return error(request)
    array = UpdatePerfil(request)
    return JsonResponse(array, safe=False, status=200)

    
#CADASTRAR PARCEIROS
@login_required
def cadastrePartnesViews(request):
    if allowPage(request, "register_partners") == False:
        return error(request)
    SsearchCategoria = searchCategoria(request)
    searchUnity = searchUnit(request)
    return render(request, 'manage/cadastre/Perfis/cadastrePartnes.html', {"arr_SearchCategoria": SsearchCategoria,  "arr_SearchUnit": searchUnity})


#API CADASTRAR USUARIOS
@login_required
def ApiCadastreUser(request):
    array = CadastreUser(request)
    return JsonResponse(array, safe=False, status=200)

#API CADASTRAR PARCEIROS
@login_required
def ApiCadastrePartners(request):
    array = CadastrePartners(request)
    return JsonResponse(array, safe=False, status=200)


#CADASTRAR INDICAÇÃO
@login_required
def cadastreIndicationViews(request):
    if allowPage(request, "register_indication") == False:
        return error(request)
    sSelect_conv =  SelectConvenio(request)
    return render(request, 'manage/cadastre/Perfis/cadastreIndication.html', {"arr_SelectConvenio": sSelect_conv})

    
#API CADASTRAR INDICAÇÃO
@login_required
def ApiCadastreIndication(request):
    array = CadastreIndication(request)
    return JsonResponse(array, safe=False, status=200)


#API FORMATAR CPF
@login_required
def apiFormatCPF(request):
    array = formatcpfcnpj(request)
    return JsonResponse(array, safe=False, status=200)

     
#API FORMATAR NÚMERO DE TEL
@login_required
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
@login_required
def ApiCadastreConvenio(request):
    array =  cadastreConv(request)
    return JsonResponse(array, safe=False, status=200)

#API ATUALIZAR STATUS CONVENIO
@login_required
def ApiChangeStatusConvenio(request):
    array =  ApiChangeStatusConvenioFunction(request)
    return JsonResponse(array, safe=False, status=200)


#API PERMISSOES USERS
@login_required
def ApiPermissionsUsers(request):
    array =  allowPage(request, "")
    return JsonResponse(array, safe=False, status=200)

    
#AGENDAR COLETA
@login_required
def schedulePickupViews(request):
    if allowPage(request, "agendar_coleta") == False:
        return error(request)
    SsearchNurse =  searchNurse(request)
    SsearchDriver =  searchDriver(request)
    sSelect_conv =  SelectConvenio(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchPacienteSe = SearchSelectSchedule(request)
    return render(request, 'manage/agenda/schedulePickup.html', {"arr_SearchNurse": SsearchNurse, "arr_SearchService": SsearchService, "arr_SearchDriver": SsearchDriver, "arr_SelectConvenio": sSelect_conv, "arr_SearchExame": SsearchExame, "arr_SearchPacienteSe": SsearchPacienteSe})

#API AGENDAR COLETA
@login_required
def ApiSchedulePickupViews(request):
    array =  FschedulePickup(request)
    return JsonResponse(array, safe=False, status=200)
    


#API AGENDAR COLETA INTERNA
@login_required
def ApiSchedulePickupIntViews(request):
    array =  FschedulePickupInt(request)
    return JsonResponse(array, safe=False, status=200)
    

#CONSULTAR COLETA AGENDADA
@login_required
def ScheduledPickupViews(request):
    if allowPage(request, "consult_agenda") == False:
        return error(request)

    SsearchDoctor = searchDoctor(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchNurse =  searchNurse(request)
    SsearchDriver =  searchDriver(request)
    SsearchConvenio =  searchConvenio(request)
    SsearchScheduledPickup =  searchScheduledPickup(request)
    SsearchColors =  ApiScheduledPickupModalViews(request)
    SsearchStatus =  FunctionStatusSelect(request)
    CountAgendamentsUni = CountAgendamentsPFunction(request)
    CountAgendamentsFrust = CountAgendamentsFFunction(request)
    CountAgendamentsConcl = CountAgendamentsCSFunction(request)
    CountAgendamentsCanc = CountAgendamentsCFunction(request)
    CountAgendamentsAtras = CountAgendamentAtrasadosFunction(request)

    return render(request, 'manage/agenda/ScheduledPickup.html', {
        "arr_SearchDoctor": SsearchDoctor, 
        "arr_SearchExame": SsearchExame, 
        "arr_SearchService": SsearchService, 
        "arr_SearchNurse": SsearchNurse, 
        "arr_SearchDriver": SsearchDriver, 
        "arr_SearConvenio": SsearchConvenio, 
        "arr_SearchScheduledPickup": SsearchScheduledPickup,  
        "arr_SearchColor": SsearchColors, 
        "arr_SearchStatus": SsearchStatus, 
        "arr_CountAgendaments": CountAgendamentsUni, 
        "arr_CountAgendamentsConlcuidos": CountAgendamentsConcl,  
        "arr_CountAgendamentsFrustrados": CountAgendamentsFrust,  
        "arr_CountAgendamentsCancelados": CountAgendamentsCanc,
        "arr_CountAgendamentsAtrasados": CountAgendamentsAtras,
        })


#API CONSULTAR COLETA
@login_required
def ApiScheduledPickupViews(request):
    array = FScheduledPickup(request)
    return JsonResponse(array, safe=False, status=200)

#API DELETAR CONVENIO
@login_required
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
    searchUnity = searchUnit(request)
    return render(request, 'manage/listers/users/listUsers.html', { "arr_SearchPerfil": searchPerfil, "arr_SearchUsersFull": arrSearchUsersFull, "arr_SearchUnit": searchUnity})


#API LISTAR USUARIOS
@login_required
def ApiListUsersViews(request):
    array = searchUsers(request)
    return JsonResponse(array, safe=False, status=200)

#MODAL USUARIO
@login_required
def ApiViewDataUserModal(request):
    array = ApiViewDataUserModalFunction(request)
    return JsonResponse(array, safe=False, status=200)

@login_required
def ApiChangeStatus(request):
    array = ApiChangeStatusFunction(request)
    return JsonResponse(array, safe=False, status=200)


#MODAL ATUALIZAR USUARIOS
@ensure_csrf_cookie
@login_required
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
    searchUnity = searchUnit(request)
    return render(request, 'manage/listers/partners/listPartners.html', {"arr_SearchCategoria": SsearchCategoria, "arr_SearchPartiners": SsearchPartiners, "arr_SearchUnit": searchUnity})


#API LISTAR PARCEIROS
@ensure_csrf_cookie
@login_required
def ApiListPartnesViews(request):
    array = searchPartiners(request)
    return JsonResponse(array, safe=False, status=200)


#MODAL PARCEIROS ADM 
@login_required
@ensure_csrf_cookie #<<<< requisitar a chave do token
def ApiViewDataPartnersModal(request):
    array = ApiViewDataPartnersModalFunction(request)
    return JsonResponse(array, safe=False, status=200)



#MODAL PARCEIROS
@login_required
@ensure_csrf_cookie #<<<< requisitar a chave do token
def ApiViewDataPartnersModalINT(request):
    array = ApiViewDataPartnersModalFunctionINT(request)
    return JsonResponse(array, safe=False, status=200)



#LISTAR PACIENTES > INDICAÇÃO
@login_required
def listIndicationViews(request):
    if allowPage(request, "list_patients") == False:
        return error(request)
    SsearchIndication = searchIndication(request)
    SsearchConvenio =  searchConvenio(request)
    SsearchConvenio =  searchConvenio(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)
    return render(request, 'manage/listers/indication/listIndication.html', {"arr_SearchIndication": SsearchIndication, "arr_SearchConvenio": SsearchConvenio, "arr_SearchTypeAnexo": SearchTypeAnexo,})



#LISTAR LEADS
@login_required
def listLeadsViews(request):
    if allowPage(request, "list_indication") == False:
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
    SsearchDoctorL =  searchDoctorLead(request)
    return render(request, 'manage/cadastre/Perfis/cadastrePatient.html', {"arr_SearchPatients": SsearchPatients,"arr_SearchConvenio": SsearchConvenio,"arr_SearchDoctorL": SsearchDoctorL})
    
    
#CADASTRAR PACIENTES
@login_required
def ApiCadastrePatientViews(request):
    array = ApiCadastrePatienteFunction(request)
    return JsonResponse(array, safe=False, status=200)
 
 
#MODAL PACIENTES
@login_required
def ApiViewDataPatientsModal(request):
    array = ApiViewDataPatientsModalFunction(request)
    return JsonResponse(array, safe=False, status=200)


#MODAL PACIENTES UPDATE
@login_required
def ApiChangePatientsModal(request):
    array = ApiChangePatientsModalFunction(request)
    return JsonResponse(array, safe=False, status=200)

#MODAL PACIENTES FILES
class FetchPatientsFiles(View):
    @staticmethod
    @login_required
    @ensure_csrf_cookie
    def get(request):
        return JsonResponse(
            FetchPatientsFilesFunction(BodyDecode(request)),
            safe=False
        )
    
    @staticmethod
    @login_required
    @ensure_csrf_cookie
    def delete(request):
        return JsonResponse(
            DeletePatientsFilesFunction(request),
            safe=False
        )


@login_required
def ApiScheduledPickupModalViews(request):
    array = SearchModalScheduled(request)
    return JsonResponse(array, safe=False, status=200)



# API STATUS CONCLUIDO
@login_required
def ApiStatusAgendaConc(request):
    array = FunctionStatusAgendaConc(request)
    return JsonResponse(array, safe=False, status=200)

@login_required
def ApiReagendarAgendaConc(request):
    array = ApiReagendarAgendaConcFunction(request)
    return JsonResponse(array, safe=False, status=200)

    
# API STATUS FRUSTRAR
@login_required
def ApiStatusAgendaFrustrado(request):
    array = FunctionStatusAgendaFrustrar(request)
    return JsonResponse(array, safe=False, status=200)
    
# API STATUS CANCELAR
@login_required
def ApiStatusAgendaCancel(request):
    array = FunctionStatusAgendaCancel(request)
    return JsonResponse(array, safe=False, status=200)


#FINANCEIRO
@login_required
#INICIAR PROCESSO
def FinancialExamsViews(request):
    if allowPage(request, "agend_concluidos") == False:
        return error(request)
    SearchCompletedExams =  searchConcluidosF(request)
    SearchStratusProgress = FunctionStatus(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)
    return render(request, 'finances/exams/exams-concl.html', {"arr_SearchCompletedExams": SearchCompletedExams, "arr_SearchStratusProgress": SearchStratusProgress, "arr_SearchTypeAnexo": SearchTypeAnexo, })

# MODAL FINANCES
@login_required
def SearchModalExams(request):
    array = SearchModalExamsFunction(request)
    return JsonResponse(array, safe=False, status=200)


# MODAL FINANCES > Remover anexo
@login_required
def ModalExamsFinanceFileRemove(request):
    array = ModalExamsFinanceFileRemoveFunction(request)
    return JsonResponse(array, safe=False, status=200)



# MODAL FINANCES > Remover anexo interno
@login_required
def ModalExamsFinanceFileRemoveInt(request):
    array = ModalExamsFinanceFileRemoveFunctionInt(request)
    return JsonResponse(array, safe=False, status=200)


# API INCIAIR PROCESSO
@login_required
def ApiStartProcess(request):
    array = FunctionStartProcess(request)
    return JsonResponse(array, safe=False, status=200)


# API MODAL
@login_required
def SearchModalExamsFinances(request):
    array = FunctionModalFinances(request)
    return JsonResponse(array, safe=False, status=200)


#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
@login_required
def SaveEditionsFinances(request):
    array = SaveEditionsFinancesFunctions(request)
    return JsonResponse(array, safe=False, status=200)


#FINALIZAR PROCESSO MODAL FINANCEIRO 
@login_required
def ApiFinalizeProcess(request):
    array = FinalizeProcessFunction(request)
    return JsonResponse(array, safe=False, status=200)

@login_required
def SearchMonthExamsConcl(request):
    array = SearchMonthExamsConclFunction(request)
    return JsonResponse(array, safe=False, status=200)

#REEMBOLSO COMPLETO - FINALIZADO aquiy
@login_required
def RefundCompletedViews(request):
    if allowPage(request, "reverse_finished") == False:
        return error(request)
    SearchRefundCompleted = searchrRefundCompletedFunction(request)
    SearchStratusProgress = FunctionStatus(request)
    return render(request, 'finances/exams/refund-completed.html',  {"arr_SearchRefundCompleted": SearchRefundCompleted, "arr_SearchStratusProgress": SearchStratusProgress} )

#INDIVIDUAL, MEUS REGISTROS
def ListerPatientsUnitViews(request): #PACIENTES
    SsearchConvenio =  searchConvenio(request)
    SsearchIndication = searchPatientsUnit(request)
    return render(request, 'myRegisters/lister/patientsUnit.html', {"arr_SearchConvenio": SsearchConvenio, "arr_SearchIndication": SsearchIndication,})
    
#INDIVIDUAL, MEUS REGISTROS
def ListerPartnersUnitViews(request): #PARCEIROS
    SsearchCategoria = searchCategoria(request)
    SsearchPartiners = TabelaPartnersUnit(request)
    return render(request, 'myRegisters/lister/partnersUnit.html', {"arr_SearchCategoria": SsearchCategoria, "arr_SearchPartiners": SsearchPartiners})

#INDIVIDUAL, MEUS REGISTROS
def ListerIndicationsUnitViews(request): #INDICAÇÕES
    SsearchLeads = searchIndicationUnit(request)
    return render(request, 'myRegisters/lister/indicationsUnit.html', {"arr_SearchLeads": SsearchLeads,})

    
#LISTAR TODOS OS LEADS 
@login_required
def LeadsViews(request): #INDICAÇÕES
    if allowPage(request, "leads_all") == False:
        return error(request)
    SsearchLeadsAll = SearchLeadsAll(request)
    CountLeadsAll = CountLeadsFunction(request)
    CountLeadsMes = CountLeadsMesFunction(request)
    CountLeadsDay = CountLeadsDayFunction(request)
    SearchStatusLead = FunctionSearchStatusLead(request)
    return render(request, 'manage/listers/lead/LEADS.html', {"arr_SearchLeadsAll": SsearchLeadsAll, "arr_SearchCountLeadsAll": CountLeadsAll, "arr_SearchCountLeadsMes": CountLeadsMes, "arr_SearchCountLeadsDay": CountLeadsDay,  "arr_SearchStatusLead": SearchStatusLead,})

    
#CADASTRAR LEAD 
@login_required
def CadatsreLeadViews(request): #INDICAÇÕES
    if allowPage(request, "register_lead") == False:
        return error(request)
    SsearchDoctorL =  searchDoctorLead(request)
    sSelect_conv =  SelectConvenio(request)
    return render(request, 'manage/cadastre/Perfis/cadastreLead.html', {"arr_SearchDoctorL": SsearchDoctorL, "arr_SelectConvenio": sSelect_conv})
 
#API CADASTRAR LEAD
@login_required
def ApiCadatsreLeadViews(request):
    array = CadastreLead(request)
    return JsonResponse(array, safe=False, status=200)

    
#API LISTAR PARCEIROS
'''@ensure_csrf_cookie
@login_required
def HistoricoViews(request):
    array = historicExamConclFunction(request)
    return JsonResponse(array, safe=False, status=200)'''


# CADASTRAR UNIDADES
@login_required
def cadastreUnitViews(request): #INDICAÇÕES
    if allowPage(request, "cadastre_unit") == False:
        return error(request)
    SearchUnidade = searchUnidadeTabela(request)
    return render(request, 'manage/cadastre/unidade/CadastreUnit.html',  {"arr_SearchUnidade": SearchUnidade})

#API CADASTRAR UNIDADES
@login_required
def ApiCadastreUnit(request):
    array =  cadastreUnit(request)
    return JsonResponse(array, safe=False, status=200)

#API ATUALIZAR STATUS UNIDADES
@login_required
def ApiChangeStatusUnit(request):
    array =  ApiChangeStatusUnitFunction(request)
    return JsonResponse(array, safe=False, status=200)

    
#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
@login_required
def SaveEditionsPatient(request):
    array = SaveEditionsPatientFunction(request)
    return JsonResponse(array, safe=False, status=200)


#REEMBOLSO NÃO ATINGIDO
@login_required
def refundNotReachedViews(request): #INDICAÇÕES
    if allowPage(request, "not_reached") == False:
        return error(request)
    SearchStatusN = FunctionStatusN(request)
    SearchNotReached=searchNotReached(request)
    return render(request, 'finances/exams/refund-notReached.html', {"arr_SearchStatusN": SearchStatusN, "arr_SearchNotReached": SearchNotReached,})



#REEMBOLSO GLOSADO
@login_required
def refundGlossesViews(request): #INDICAÇÕES
    if allowPage(request, "glosses") == False:
        return error(request)
    SearchStatusN = FunctionStatusN(request)
    SearchGlosses=searchGlosses(request)
    return render(request, 'finances/exams/refund-glosses.html', {"arr_SearchStatusN": SearchStatusN, "arr_SearchSearchGlosses": SearchGlosses,})

#AGENDAR COLETA INTERNA
@login_required
def schedulePickupIntViews(request):
    if allowPage(request, "schedule_collection_int") == False:
        return error(request)
    SsearchNurse =  searchNurse(request)
    SsearchDriver =  searchDriver(request)
    sSelect_conv =  SelectConvenio(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchPacienteSelect = SearchSelectInterno(request)
    return render(request, 'internalProcedure/schedulePickup-Int.html', {"arr_SearchNurse": SsearchNurse, "arr_SearchService": SsearchService, "arr_SearchDriver": SsearchDriver, "arr_SelectConvenio": sSelect_conv, "arr_SearchExame": SsearchExame, "arr_SearchPacienteSelect": SsearchPacienteSelect})


#CONSULTAR COLETA AGENDADA INTERNA
@login_required
def ScheduledPickupIntViews(request):
    if allowPage(request, "scheduled_collection_int") == False:
        return error(request)

    SsearchDoctor = searchDoctor(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchNurse =  searchNurse(request)
    SsearchConvenio =  searchConvenio(request)
    SsearchScheduledPickupInt =  searchScheduledPickupInt(request)
    SsearchStatus =  FunctionStatusSelect(request)
    return render(request, 'internalProcedure/ScheduledPickup-Int.html', {
        "arr_SearchDoctor": SsearchDoctor, 
        "arr_SearchExame": SsearchExame, 
        "arr_SearchService": SsearchService, 
        "arr_SearchNurse": SsearchNurse, 
        "arr_SearConvenio": SsearchConvenio, 
        "arr_SearchScheduledPickupInt": SsearchScheduledPickupInt,  
        "arr_SearchStatus": SsearchStatus,
        })

#FILTRO MES COLETA INTERNA
@login_required
def ScheduledMonthIntViews(request):
    array = SearchMonthIntFunction(request)
    return JsonResponse(array, safe=False, status=200)

#API MODAL DA COLETA AGENDADAS
@login_required
def ApiScheduledPickupModalIntViews(request):
    array = SearchModalScheduledInt(request)
    return JsonResponse(array, safe=False, status=200)


# API STATUS CONCLUIDO
@login_required
def ApiStatusAgendaConcInt(request):
    array = FunctionStatusAgendaConcInt(request)
    return JsonResponse(array, safe=False, status=200)


#FINANCEIRO INTERNO
@login_required
#SOLICITAÇÃO DE REEMBOLSO
def SolicitationsRetfund(request):
    if allowPage(request, "refund_int") == False:
        return error(request)
    SearchExams =  RetfundFConcl(request)
    SearchStratusProgress = FunctionStatus(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)
    return render(request, 'internalProcedure/SolicitationsRefund.html', {"arr_SearchInicioExams": SearchExams, "arr_SearchStratusProgress": SearchStratusProgress, "arr_SearchTypeAnexo": SearchTypeAnexo, })



@login_required
#PROCESSOS FINALIZADOS >> INTERNO
def RefundCompletedInternoViews(request):
    if allowPage(request, "reverse_finished_int") == False:
        return error(request)
    SearchExamsFim =  RetfundFFinalizado(request)
    SearchStratusProgress = FunctionStatus(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)
    return render(request, 'internalProcedure/refund-completed-int.html', {"arr_SearchCompletedExamsFinalizado": SearchExamsFim, "arr_SearchStratusProgress": SearchStratusProgress, "arr_SearchTypeAnexo": SearchTypeAnexo, })

    
@login_required
def SearchMonthFInalizadosInt(request):
    array = pesqMesInternoFinalizados(request)
    return JsonResponse(array, safe=False, status=200)

    
@login_required
def SearchMonthExamsSolicitationViews(request):
    array = SearchMonthSolicitation(request)
    return JsonResponse(array, safe=False, status=200)

@login_required
def SearchMonthExamsRefund(request):
    array = SearchMonthExamsRefundF(request)
    return JsonResponse(array, safe=False, status=200)


#FECHAMENTO PARCEIROS
@login_required
def ClosingPartnersViews(request): #INDICAÇÕES
    if allowPage(request, "fechamento_parceiro") == False:
        return error(request)
    ClosingPartners = TableClosingPartners(request)
    valTotalPartiners = valTotalPartinersF(request)
    return render(request, 'finances/closure/ClosingPartners.html', {"arr_SearchClosingPartners": ClosingPartners, "arr_valTotalPartiners": valTotalPartiners,})

@login_required
def SearchMonthClosingPartners(request):
    array = FilterMonthClosingPartners(request)
    return JsonResponse(array, safe=False, status=200)



@login_required
def paymentDetails(request):
    array = searchNotAtingeClosingPartners(request)
    return JsonResponse(array, safe=False, status=200)



@login_required
def payPartnersV(request):
    array = payPartnersVFunction(request)
    return JsonResponse(array, safe=False, status=200)



@login_required
def SearchInfoM(request):
    array = SearchInfoFunction(request)
    return JsonResponse(array, safe=False, status=200)



    
# FECHAMENTO COMERCIAL
@login_required
def ClosingCommercialViews(request): #INDICAÇÕES
    if allowPage(request, "fechamento_comercial") == False:
        return error(request)
    ClosingCommercial = TableClosingCommercial(request)
    valTotalCommercial = valTotalCommercialFunction(request)
    return render(request, 'finances/closure/ClosingCommercial.html',  {"arr_SearchClosingCommercial": ClosingCommercial, "arr_valTotalCommercial": valTotalCommercial,})

#FILTRO MES FECHAMENTO COMERCIAL
@login_required
def SearchMonthClosingCommercial(request):
    array = FilterMonthClosingCommercial(request)
    return JsonResponse(array, safe=False, status=200)
 

@login_required
def paymentDetailsCommercial(request):
    array = searchNotAtingeClosingCommercial(request)
    return JsonResponse(array, safe=False, status=200)



@login_required
def SearchInfoCommercial(request):
    array = SearchInfoCommercialFunction(request)
    return JsonResponse(array, safe=False, status=200)

#PAGAMENTO COMERCIAL
@login_required
def payCommercial(request):
    array = payCommercialFunction(request)
    return JsonResponse(array, safe=False, status=200)


#ROTA DAS ENFERMEIRAS
@login_required
def CollectionRouteViews(request): 
    if allowPage(request, "collection_route") == False:
        return error(request)
    SearchTypeAnexo =  FunctionSearchTypeAnexo(request)
    SsearchRoute =  searchRouteNurse(request)
    return render(request, 'manage/agenda/collectionRoute.html', {"arr_SearchTypeAnexo": SearchTypeAnexo , "arr_SearchRoute": SsearchRoute})



#INICIAR COLETA - ENFERMEIRA
@login_required
def ApiIniciarColeta(request):
    array = IniciarColetaFunction(request)
    return JsonResponse(array, safe=False, status=200)
    

#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
@login_required
def SaveAnexo(request):
    array = SaveAnexoFunction(request)
    return JsonResponse(array, safe=False, status=200)



#FECHAMENTO ENFERMEIRAS - OUTROS
@login_required
def closingInt(request):
    if allowPage(request, "fechamento_interno") == False:
        return error(request)
    ClosingInt = TableClosingInt(request)
    return render(request, 'finances/closure/ClosingInt.html', {"arr_SearchClosingInt": ClosingInt,})



@login_required
def SearchClosingIntFilter(request):
    array = TableClosingIntFilter(request)
    return JsonResponse(array, safe=False, status=200)


#MEU FECHAMENTO
@login_required
def ClosingFinanceUnit(request):
    if allowPage(request, "meu_fechamento") == False:
        return error(request)
    ClosingUnit = SearchFinanceInt(request)
    ClosingUnitAG = SearchFinanceIntAgendado(request)
    ClosingUnitAN = ClosingUnitAnalise(request)
    SearchFinanceIntGNA = SearchFinanceIntGlosa(request)
    ClosingUnitResultPG = ClosingUnitResult(request)
    return render(request, 'myRegisters/lister/closingUnit.html', 
    {"arr_SearchClosingUnit": ClosingUnit, 
    "arr_SearchClosingUnitAG": ClosingUnitAG, 
    "arr_SearchClosingUnitAN": ClosingUnitAN, 
    "arr_SearchClosingUnitGNA": SearchFinanceIntGNA,
    "arr_SearchClosingUnitResultPG": ClosingUnitResultPG,})




#Informações do Login
@login_required
def LogUser(request):
    InfoLog = iInfoLog(request)
    return render(request, 'templates/base.html', {"arr_SearchInfoLog": InfoLog,})



#API SALVAR STATUS NEGATIVO LEAD
@login_required
def ApiStatusNegative(request):
    array = StatusNegative(request)
    return JsonResponse(array, safe=False, status=200)


#API FILTRO DE STATUS SLEAD
@login_required
def SearchStatusLeadFilter(request):
    array = SearchStatusLeadFilterFunction(request)
    return JsonResponse(array, safe=False, status=200)


def createUsers():
    e = 0
    c = 0
    with connections['auth_users'].cursor() as cursor:
        
        query = "SELECT perfil, cpf, nome, email, login, data_regis FROM auth_users.users"
        cursor.execute(query)
        dados = cursor.fetchall()
        arr_response = [
            {
                "name": nome,
                "email": email,
                "username": login,
                "password": str(datetime.strptime(str(data_regis), "%Y-%m-%d").strftime("%d%Y")) if str(perfil) == 7 else str(cpf)
            } for perfil, cpf, nome, email, login, data_regis in dados
        ]

        for key in arr_response:
            print(key)
            firstname = key.get('name', '')
            id_user = key.get('username', None)
            email = key.get('email', '')
            id_pass = key.get('password', '')
            lastname = ''

            if User.objects.filter(username=id_user).exists():
                user = User.objects.get(username=id_user)
                user.first_name = firstname
                user.last_name = ''
                user.email = email

                user.save()
                e += 1
            else:
                user = User.objects.create_user(username=id_user, email=email, first_name=firstname, last_name=lastname, password=id_pass)
                c += 1

    array = {
        "quantity_exists": e,
        "quantity_create": c
    }
    
    print(array)
    return True