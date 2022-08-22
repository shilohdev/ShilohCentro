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
from django.db.models import Q
from requests import request
from auth_users.decorator import RecontatoFunction, FileContractFunction, ContractCollectionFunction, HistoricoParceiros, HistoryIndicationFunction, ApiAdjustRouteFunction, searchAdjustRouteNurse, FilePhotoViewFunction, PhotoProfileFunction, ApichangeUserProfileFunction, DataMyProfileViews, ApiNewRegisPatientFunction, ApiAttPartnersFunction, searchComercialFunction, PrePartnerCancelFunction, CadastrePrePartners, RemoveFilePartnersFunction, FetchPartnersFilesFunction, ApiGerFilePartnersFunction, ApiNfPartnersFunction, ApiViewDataPartnersModalFunctionINT, errors, ModalExamsFinanceFileRemoveFunctionInt, SearchStatusLeadFilterFunction, FunctionSearchStatusLead, StatusNegative, iInfoLog, searchRouteNurse, searchUnidadeTabela, RetfundFFinalizado, RetfundFConcl, SearchMonthIntFunction, FunctionStatusAgendaConcInt, SearchModalScheduledInt, searchScheduledPickupInt, FschedulePickupInt, SearchSelectInterno, CountAgendamentAtrasadosFunction, CountAgendamentsCFunction, CountAgendamentsCSFunction, CountAgendamentsFFunction, CountAgendamentsPFunction,  CountLeadsDayFunction, CountLeadsMesFunction, CountLeadsFunction, SaveEditionsPatientFunction, searchUnit, ApiChangeStatusUnitFunction, cadastreUnit, UpdatePerfil, CadastreLead, SearchLeadsAll, searchIndicationUnit, TabelaPartnersUnit, searchPatientsUnit, ModalExamsFinanceFileRemoveFunction, SearchModalExamsFunction, FunctionStartProcess, FunctionSearchTypeAnexo, FunctionStatus, FunctionStatusSelect, FunctionStatusAgendaCancel, FunctionStatusAgendaFrustrar,ApiReagendarAgendaConcFunction, FunctionStatusAgendaConc, SearchModalScheduled, searchScheduledPickup, SearchSelectSchedule, DeletePatientsFilesFunction, FetchPatientsFilesFunction, ApiChangePatientsModalFunction,searchLead, SelectConvenio, ApiViewDataPatientsModalFunction, ApiCadastrePatienteFunction, searchLeads, searchIndication, searchUsers, ApiChangeUsersModalFunction, ApiViewDataPartnersModalFunction, ApiChangeStatusFunction, ApiViewDataUserModalFunction,TabelaPartners, SearchUsersFull, DeleteConv, FScheduledPickup, searchService, searchDoctor, searchExame, FschedulePickup, CadastreUser, CadastrePartners, CadastreIndication, formatcpfcnpj, formatTEL, ApiChangeStatusConvenioFunction, cadastreConv, error, allowPage, searchTPerfil, searchCategoria, searchNurse, searchDriver, searchConvenio
from auth_finances.functions.exams.models import Total_Partners_Function, ClosingInternoFiltro_Function, SearchClosingInterno_Function, Interno_Total_Function, Interno_ApagarShilohLab_Function, Interno_ApagarLabMovel_Function, Pago_ShilohLab_Interno_Function, Pago_LabMovel_Interno_Function, Commerce_total_Function, Commerce_ApagarLabMovel_Function, Commerce_ApagarShilohLab_Function, Commerce_PagosShilohLab_Function, ShilohLab_APagarFunction, LabMovel_APagarFunction, PagoShilohLabFunction, PagoLabMovelFunction, Pago_LabMovel_Comercial_Function, AnxDoc, FunctionDashCardNFs, FunctionDashFinanceTableYear, FunctionDashFinanceTable, FunctionDashOutros, FunctionCardReembolsado, FunctionDashCardWorkLab, FunctionDashCardAlvaro, FunctionDashGeralFinalizados, FunctionDashGeralPendente, FunctionDashPago, FunctionDashAndamento, FunctionDashAnalise, FunctionDashPendente, ClosingUnitResult, ClosingUnitAnalise, SearchFinanceIntGlosa, SearchFinanceIntAgendado, SearchFinanceInt, SaveAnexoFunction, payCommercialFunction, SearchInfoCommercialFunction, searchNotAtingeClosingCommercial, FilterMonthClosingCommercial, TableClosingCommercial, SearchInfoFunction, payPartnersVFunction, searchClosingPartners, FilterMonthClosingPartners, TableClosingPartners, SearchMonthSolicitation, pesqMesInternoFinalizados, FinalizeProcessFunction, SaveEditionsFinancesFunctions, FunctionModalFinances
from auth_dash.functions import CountDashTotalFunction, DashCommerceMonthFunction, DashCommerceDayFunction, RankingCommerceMonthFunction, RankingCommerceDayFunction, DashProdutividadePacienteFunction, DashProdutividadeAgendamentoFunction, DashCollectionConcluidoMesFunction, DashCollectioAndamentoMesFunction, DashCollectionPendenteMesFunction, DashCollectionConcluidoDiaFunction, DashCollectioAndamentoDiaFunction, DashCollectionPendenteDiaFunction, RankingEnfermagemMonthFunction, RankingEnfermagemDayFunction, RankingDashAtenMonthFunction, PhotoRankByArrayFunction, _treating_data, RankingDashAtenDayFunction, PhotoRankFunction
from .models import Users
from functions.general.decorator import BodyDecode
from auth_permissions.decorator import CreatePermissionAll
import base64
import json
import time
from re import A
from functions.module_clicksign.decorator import ModuleSendClickSignFunction



def FotoProfile(request):
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'pages/home.html',
    {
        "arr_ViewFoto": ViewFoto,
    })



def csrf_failure(request, reason=""):
    raise PermissionDenied()

#ATUALIZAR USUARIO INTERNO
@login_required
def ApiCreatePermissionAll(request):
    array = CreatePermissionAll(request)
    return JsonResponse(array, safe=False, status=200)



#CADASTRAR USUARIO
@login_required
def cadastreUserViews(request):
    if allowPage(request, "register_user") == False:
        return error(request)
    searchPerfil = searchTPerfil(request)
    searchUnity = searchUnit(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/cadastre/Perfis/cadastreUser.html', 
    {"arr_SearchPerfil": searchPerfil,  
    "arr_SearchUnit": searchUnity,
    "arr_ViewFoto": ViewFoto,

    })

    
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
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'manage/cadastre/Perfis/cadastrePartnes.html', 
    {"arr_SearchCategoria": SsearchCategoria,  "arr_SearchUnit": searchUnity, "arr_ViewFoto": ViewFoto,})


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
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'manage/cadastre/Perfis/cadastreIndication.html', {"arr_ViewFoto": ViewFoto, "arr_SelectConvenio": sSelect_conv})

    
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
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'manage/cadastre/Convenio/cadastreConvenio.html', { "arr_ViewFoto": ViewFoto, "arr_SearchConvenio": SsearchConvenio,})

    
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
    SsearchDriver =  searchDriver(request)
    sSelect_conv =  SelectConvenio(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
    SsearchPacienteSe = SearchSelectSchedule(request)
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'manage/agenda/schedulePickup.html',
     {
        "arr_ViewFoto": ViewFoto,
         "arr_SearchService": SsearchService, 
         "arr_SearchDriver": SsearchDriver, 
         "arr_SelectConvenio": sSelect_conv, 
         "arr_SearchExame": SsearchExame, 
         "arr_SearchPacienteSe": SsearchPacienteSe
    })

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

    nurse_active = Users.objects.order_by('-data_regis').filter(status='Ativo', perfil='3')

    SsearchDoctor = searchDoctor(request)
    SsearchExame = searchExame(request)
    SsearchService = searchService(request)
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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/agenda/ScheduledPickup.html', {
        "arr_SearchDoctor": SsearchDoctor, 
        "arr_SearchExame": SsearchExame, 
        "arr_SearchService": SsearchService, 
        "arr_SearchNurse_Active": nurse_active, 
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
        "arr_ViewFoto": ViewFoto,

        })


#API CONSULTAR COLETA >> Filtro mês
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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/listers/users/listUsers.html', 
    {
        "arr_ViewFoto": ViewFoto,
        "arr_SearchPerfil": searchPerfil,
        "arr_SearchUsersFull": arrSearchUsersFull,
        "arr_SearchUnit": searchUnity
    })


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
    SearchComercial = searchComercialFunction(request)
    ViewFoto = FilePhotoViewFunction(request)
    
    return render(request, 'manage/listers/partners/listPartners.html', 
    {
        "arr_SearchCategoria": SsearchCategoria, 
        "arr_SearchPartiners": SsearchPartiners,
        "arr_SearchUnit": searchUnity,
        "arr_SearchComercial": SearchComercial,
        "arr_ViewFoto": ViewFoto,
    })
 


#MODAL PARCEIROS ADM 
@login_required
@ensure_csrf_cookie #<<<< requisitar a chave do token
def ApiViewDataPartnersModal(request):
    array = ApiViewDataPartnersModalFunction(request)
    return JsonResponse(array, safe=False, status=200)

#MODAL PARCEIROS INTERNO 
@login_required
@ensure_csrf_cookie #<<<< requisitar a chave do token
def ApiViewDataPartnersModalint(request):
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
    ViewFoto = FilePhotoViewFunction(request)
    
    return render(request, 'manage/listers/indication/listIndication.html', 
    {
        "arr_ViewFoto": ViewFoto,
        "arr_SearchIndication": SsearchIndication, 
        "arr_SearchConvenio": SsearchConvenio, 
        "arr_SearchTypeAnexo": SearchTypeAnexo,
    })



#LISTAR LEADS
@login_required
def listLeadsViews(request):
    if allowPage(request, "list_indication") == False:
        return error(request) 
    SsearchLeads = searchLead(request)
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'manage/listers/lead/listLead.html', {"arr_ViewFoto": ViewFoto, "arr_SearchLeads": SsearchLeads, })


#CADASTRAR PACIENTE
@login_required
def CadastrePatientViews(request):
    if allowPage(request, "cadastre_patients") == False:
        return error(request)
    SsearchPatients = searchLeads(request)  
    SsearchConvenio =  searchConvenio(request)
    ViewFoto = FilePhotoViewFunction(request)
    doctor_active = Users.objects.order_by('-data_regis').filter(Q(status='Ativo') | Q(status='Inativo'))

    return render(request, 'manage/cadastre/Perfis/cadastrePatient.html', 
    {"arr_SearchPatients": SsearchPatients,
    "arr_SearchConvenio": SsearchConvenio,
    "arr_SearchDoctorL": doctor_active,
    "arr_ViewFoto": ViewFoto,
    })
    
    
#CADASTRAR PACIENTES LEAD
@login_required
def ApiCadastrePatientViews(request):
    array = ApiCadastrePatienteFunction(request)
    return JsonResponse(array, safe=False, status=200)
 

#CADASTRAR PACIENTES NOVO REGISTRO
@login_required
def ApiNewRegisPatient(request):
    array = ApiNewRegisPatientFunction(request)
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

#INDIVIDUAL, MEUS REGISTROS
def ListerPatientsUnitViews(request): #PACIENTES
    SsearchConvenio =  searchConvenio(request)
    SsearchIndicationUnit = searchPatientsUnit(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'myRegisters/lister/patientsUnit.html', 
    {"arr_ViewFoto": ViewFoto,
    "arr_SearchConvenio": SsearchConvenio,
    "arr_SearchIndication": SsearchIndicationUnit,
    })
    

#INDIVIDUAL, MEUS REGISTROS
def ListerPartnersUnitViews(request): #PARCEIROS
    SsearchCategoria = searchCategoria(request)
    SsearchPartiners = TabelaPartnersUnit(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'myRegisters/lister/partnersUnit.html', 
    {
        "arr_SearchCategoria": SsearchCategoria, 
        "arr_SearchPartiners": SsearchPartiners,
        "arr_ViewFoto": ViewFoto,

    })

#INDIVIDUAL, MEUS REGISTROS
def ListerIndicationsUnitViews(request): #INDICAÇÕES
    SsearchLeads = searchIndicationUnit(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'myRegisters/lister/indicationsUnit.html', 
    {
        "arr_ViewFoto": ViewFoto,
        "arr_SearchLeads": SsearchLeads,
    })

    
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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/listers/lead/LEADS.html', 
    {"arr_SearchLeadsAll": SsearchLeadsAll,
    "arr_SearchCountLeadsAll": CountLeadsAll,
    "arr_SearchCountLeadsMes": CountLeadsMes,
    "arr_SearchCountLeadsDay": CountLeadsDay, 
    "arr_SearchStatusLead": SearchStatusLead,
    "arr_ViewFoto": ViewFoto,

    })

    
#CADASTRAR LEAD 
@login_required
def CadatsreLeadViews(request): #INDICAÇÕES
    if allowPage(request, "register_lead") == False:
        return error(request)
    doctor_active = Users.objects.order_by('-data_regis').filter(Q(status='Ativo') | Q(status='Inativo'))
    sSelect_conv =  SelectConvenio(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/cadastre/Perfis/cadastreLead.html', 
    {"arr_SearchDoctorL": doctor_active, 
    "arr_SelectConvenio": sSelect_conv, 
    "arr_ViewFoto": ViewFoto,
    })
 
#API CADASTRAR LEAD
@login_required
def ApiCadatsreLeadViews(request):
    array = CadastreLead(request)
    return JsonResponse(array, safe=False, status=200)



# CADASTRAR UNIDADES
@login_required
def cadastreUnitViews(request): #INDICAÇÕES
    if allowPage(request, "cadastre_unit") == False:
        return error(request)
    SearchUnidade = searchUnidadeTabela(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/cadastre/unidade/CadastreUnit.html',  
    {
        "arr_SearchUnidade": SearchUnidade,
        "arr_ViewFoto": ViewFoto,
    })

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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'internalProcedure/schedulePickup-Int.html', 
    {
        "arr_SearchNurse": SsearchNurse, 
        "arr_SearchService": SsearchService, 
        "arr_SearchDriver": SsearchDriver, 
        "arr_SelectConvenio": sSelect_conv, 
        "arr_SearchExame": SsearchExame, 
        "arr_SearchPacienteSelect": SsearchPacienteSelect,
        "arr_ViewFoto": ViewFoto,

    })


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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'internalProcedure/ScheduledPickup-Int.html', {
        "arr_SearchDoctor": SsearchDoctor, 
        "arr_SearchExame": SsearchExame, 
        "arr_SearchService": SsearchService, 
        "arr_SearchNurse": SsearchNurse, 
        "arr_SearConvenio": SsearchConvenio, 
        "arr_SearchScheduledPickupInt": SsearchScheduledPickupInt,  
        "arr_SearchStatus": SsearchStatus,
        "arr_ViewFoto": ViewFoto,

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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'internalProcedure/SolicitationsRefund.html', 
    {"arr_SearchInicioExams": SearchExams, 
    "arr_SearchStratusProgress": SearchStratusProgress, 
    "arr_SearchTypeAnexo": SearchTypeAnexo,
    "arr_ViewFoto": ViewFoto,
    })



@login_required
#PROCESSOS FINALIZADOS >> INTERNO
def RefundCompletedInternoViews(request):
    if allowPage(request, "reverse_finished_int") == False:
        return error(request)
    SearchExamsFim =  RetfundFFinalizado(request)
    SearchStratusProgress = FunctionStatus(request)
    SearchTypeAnexo = FunctionSearchTypeAnexo(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'internalProcedure/refund-completed-int.html', 
    {"arr_SearchCompletedExamsFinalizado": SearchExamsFim,
     "arr_SearchStratusProgress": SearchStratusProgress,
      "arr_SearchTypeAnexo": SearchTypeAnexo,
      "arr_ViewFoto": ViewFoto, 
      })

    
@login_required
def SearchMonthFInalizadosInt(request):
    array = pesqMesInternoFinalizados(request)
    return JsonResponse(array, safe=False, status=200)

    
@login_required
def SearchMonthExamsSolicitationViews(request):
    array = SearchMonthSolicitation(request)
    return JsonResponse(array, safe=False, status=200)


#FECHAMENTO PARCEIROS
@login_required
def ClosingPartnersViews(request): #INDICAÇÕES
    if allowPage(request, "fechamento_parceiro") == False:
        return error(request)
    ClosingPartners = TableClosingPartners(request)
    Total = Total_Partners_Function(request)

    ViewFoto = FilePhotoViewFunction(request)
    LabMovel_Pago = PagoLabMovelFunction(request)
    ShilohLab_Pago = PagoShilohLabFunction(request)
    LabMovel_APagar = LabMovel_APagarFunction(request)
    ShilohLab_APagar = ShilohLab_APagarFunction(request)

    return render(request, 'finances/closure/ClosingPartners.html', 
    {
        "arr_SearchClosingPartners": ClosingPartners, 
        "arr_ViewFoto": ViewFoto,
        "arr_LabMovel_Pago": LabMovel_Pago,
        "arr_ShilohLab_Pago": ShilohLab_Pago,
        "arr_LabMovel_APagar": LabMovel_APagar,
        "arr_ShilohLab_APagar": ShilohLab_APagar,
        "arr_Total": Total,
    })


@login_required
def SearchMonthClosingPartners(request):
    array = FilterMonthClosingPartners(request)
    return JsonResponse(array, safe=False, status=200)


@login_required
def paymentDetails(request):
    array = searchClosingPartners(request)
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

    ViewFoto = FilePhotoViewFunction(request)
    Pago_LabMovel_Comercial = Pago_LabMovel_Comercial_Function(request)
    Pago_ShilohLab_Comercial = Commerce_PagosShilohLab_Function(request)
    Apagar_LabMovel_Comercial = Commerce_ApagarLabMovel_Function(request)
    Apagar_ShilohLab_Comercial = Commerce_ApagarShilohLab_Function(request)
    Total_Commerce = Commerce_total_Function(request)
    ClosingCommercial = TableClosingCommercial(request)

    return render(request, 'finances/closure/ClosingCommercial.html',  
    {
        "arr_ViewFoto": ViewFoto,
        "arr_Commerce_LabMovel_Pago": Pago_LabMovel_Comercial,
        "arr_Commerce_ShilohLab_Pago": Pago_ShilohLab_Comercial,
        "arr_Commerce_LabMovel_Apagar": Apagar_LabMovel_Comercial,
        "arr_Commerce_ShilohLab_Apagar": Apagar_ShilohLab_Comercial,
        "arr_Commerce_Total_Comercial": Total_Commerce,
        "arr_SearchClosingCommercial": ClosingCommercial,
    })


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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'manage/agenda/collectionRoute.html', 
    {
        "arr_SearchTypeAnexo": SearchTypeAnexo , 
        "arr_SearchRoute": SsearchRoute,
        "arr_ViewFoto": ViewFoto,
        })



#INICIAR COLETA - ENFERMEIRA
@login_required
def ApiIniciarColeta(request):
    array = ModuleSendClickSignFunction(request)
    return JsonResponse(array, safe=False, status=200)
    

#Salvar anexo 
@login_required
def SaveAnexo(request):
    array = SaveAnexoFunction(request)
    return JsonResponse(array, safe=False, status=200)


#FECHAMENTO INTERNO 
@login_required
def ClosingInternoViews(request): #INDICAÇÕES
    if allowPage(request, "fechamento_interno") == False:
        return error(request)

    ViewFoto = FilePhotoViewFunction(request)
    Pago_LabMovel_Interno = Pago_LabMovel_Interno_Function(request)
    Pago_ShilohLab_Interno = Pago_ShilohLab_Interno_Function(request)
    Apagar_LabMovel_Interno = Interno_ApagarLabMovel_Function(request)
    Apagar_ShilohLab_Interno = Interno_ApagarShilohLab_Function(request)
    Interno_Total = Interno_Total_Function(request)
    SearchClosingInterno = SearchClosingInterno_Function(request)

    return render(request, 'finances/closure/ClosingInt.html',  
    {
        "arr_ViewFoto": ViewFoto,
        "arr_Interno_LabMovel_Pago": Pago_LabMovel_Interno,
        "arr_Interno_ShilohLab_Pago": Pago_ShilohLab_Interno,
        "arr_Interno_LabMovel_Apagar": Apagar_LabMovel_Interno,
        "arr_Interno_ShilohLab_Apagar": Apagar_ShilohLab_Interno,
        "arr_Interno_Total": Interno_Total,
        "arr_SearchClosingInterno": SearchClosingInterno,
        
    })


@login_required
def ClosingInternoFiltro(request):
    array = ClosingInternoFiltro_Function(request)
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
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'myRegisters/lister/closingUnit.html', 
    {
        "arr_SearchClosingUnit": ClosingUnit, 
        "arr_SearchClosingUnitAG": ClosingUnitAG, 
        "arr_SearchClosingUnitAN": ClosingUnitAN, 
        "arr_SearchClosingUnitGNA": SearchFinanceIntGNA,
        "arr_SearchClosingUnitResultPG": ClosingUnitResultPG,
        "arr_ViewFoto": ViewFoto,
    
    })





#Informações do Login
@login_required
def LogUser(request):
    InfoLog = iInfoLog(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'templates/base.html', {"arr_SearchInfoLog": InfoLog, "arr_ViewFoto": ViewFoto,})



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




#ANEXO NF- PARCEIROS SALVAR FILE
@login_required
def ApiNfPartners(request):
    array = ApiNfPartnersFunction(request)
    return JsonResponse(array, safe=False, status=200)


#ANEXO NF- PARCEIROS
@login_required
def ApiGerFilePartners(request):
    array = ApiGerFilePartnersFunction(request)
    return JsonResponse(array, safe=False, status=200)


#NOTA FISCAL PARCEIROS
class FetchPartnersFiles(View):
    @staticmethod
    @login_required
    @ensure_csrf_cookie
    def get(request):
        return JsonResponse(
            FetchPartnersFilesFunction(BodyDecode(request)),
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


# MODAL FINANCES > Remover anexo partners
@login_required
def RemoveFilePartners(request):
    array = RemoveFilePartnersFunction(request)
    return JsonResponse(array, safe=False, status=200)



@login_required
def DashboardsRefunds(request):
    if allowPage(request, "dash_reimbursement") == False:
        return error(request)
    DashPendente = FunctionDashPendente(request)
    DashAnalise = FunctionDashAnalise(request)
    DashAndamento = FunctionDashAndamento(request)
    DashPago = FunctionDashPago(request)
    DashGeralPendente = FunctionDashGeralPendente(request)
    DashGeralFinanceiro = FunctionDashGeralFinalizados(request)
    DashCardAlvaro = FunctionDashCardAlvaro(request)
    DashCardWorkLab = FunctionDashCardWorkLab(request)
    DashCardReembolsado = FunctionCardReembolsado(request)
    DashOutros = FunctionDashOutros(request)
    DashFinanceTable = FunctionDashFinanceTable(request)
    DashFinanceTableYear = FunctionDashFinanceTableYear(request)
    DashCardNFs = FunctionDashCardNFs(request)
    ViewFoto = FilePhotoViewFunction(request)

    return render(request, 'dashboards/dash_finances/dash_management.html', 
    {
        "arr_DashPendentes": DashPendente, 
        "arr_DashAnalise": DashAnalise,
        "arr_DashAndamento": DashAndamento,
        "arr_DashPago": DashPago,
        "arr_DashCardNFs": DashCardNFs,
        "arr_DashOutros":DashOutros,
        "arr_DashGeralPendente": DashGeralPendente,
        "arr_DashGeralFinanceiro": DashGeralFinanceiro,
        "arr_DashCardAlvaro": DashCardAlvaro,
        "arr_DashCardWorkLab": DashCardWorkLab,
        "arr_DashCardReembolsado": DashCardReembolsado,
        "arr_DashFinanceTable": DashFinanceTable,
        "arr_DashFinanceTableYear": DashFinanceTableYear,
        "arr_ViewFoto": ViewFoto,

    })



#API PRÉ-CADASTRAR PARCEIROS
@login_required
def ApiCadastrePrePartners(request):
    array = CadastrePrePartners(request)
    return JsonResponse(array, safe=False, status=200) 


#API PRÉ-CADASTRAR CANCELAR
@login_required
def PrePartnerCancel(request):
    array = PrePartnerCancelFunction(request)
    return JsonResponse(array, safe=False, status=200) 
    



#MEUS PARCEIROS
@login_required
def ApiAttPartners(request):
    array = ApiAttPartnersFunction(request)
    return JsonResponse(array, safe=False, status=200) 

    


#ANEXAR ARQUIVO
@login_required
def ApiAnexarFiles(request):
    array = AnxDoc(request)
    return JsonResponse(array, safe=False, status=200) 


#MEU PERFIL
@login_required
def MyProfileViews(request):
    SsearchProfile = DataMyProfileViews(request)
    ViewFoto = FilePhotoViewFunction(request)
    return render(request, 'myRegisters/myProfile/myProfile.html', 
    {
        "arr_SearchProfile": SsearchProfile,
        "arr_ViewFoto": ViewFoto,

    })


#API MEU PERFIL
@login_required
def ApichangeUserProfile(request):
    array = ApichangeUserProfileFunction(request)
    return JsonResponse(array, safe=False, status=200)


#FOTO MEU PERFIL
@login_required
def ApiPhotoProfile(request):
    array = PhotoProfileFunction(request)
    return JsonResponse(array, safe=False, status=200)


#FOTO MEU PERFIL
@login_required
def FilePhotoView(request):
    array = FilePhotoViewFunction(request)
    return JsonResponse(array, safe=False, status=200)



#DASHBOARD COMERCIAL
@login_required
def DashCommercialViews(request): 
    if allowPage(request, "ranking_comercial") == False:
        return error(request)
    ViewFoto = FilePhotoViewFunction(request)#foto perfil parte superior

    CountDashTotal = CountDashTotalFunction(request)
    DashCommerceMonth = DashCommerceMonthFunction(request)
    DashCommerceDay = DashCommerceDayFunction(request)
    RankingCommerceDay = RankingCommerceDayFunction(request)
    RankingCommerceMonth = RankingCommerceMonthFunction(request)
    
    PhotoRankingday = PhotoRankByArrayFunction(RankingCommerceDay)
    PhotoRankingMonth = PhotoRankByArrayFunction(RankingCommerceMonth)

    data_ranking_atendimento_dia = _treating_data(ranking=RankingCommerceDay, photo=PhotoRankingday)
    data_ranking_atendimento_mes = _treating_data(ranking=RankingCommerceMonth, photo=PhotoRankingMonth)



    return render(request, 'dashboards/ranking/DashCommercial.html', 
    {
        "arr_ViewFoto": ViewFoto,
         "arr_SearchCountDashTotal": CountDashTotal,
         "arr_DashCommerceMonth": DashCommerceMonth,
         "arr_DashCommerceDay": DashCommerceDay,
         "arr_RankingCommerceDay": RankingCommerceDay,
         "arr_RankingCommerceMonth": RankingCommerceMonth,
    } )
 

#DASHBOARD ATENDIMENTO
@login_required
def DashServiceViews(request): 
    if allowPage(request, "ranking_atendimento") == False:
        return error(request)
    ViewFoto = FilePhotoViewFunction(request)#foto perfil parte superior
    
    RankingDashAtenDay = RankingDashAtenDayFunction(request)
    RankingDashAtenMonth = RankingDashAtenMonthFunction(request)
    RankingEnfermagemDay = RankingEnfermagemDayFunction(request)
    RankingEnfermagemMonth = RankingEnfermagemMonthFunction(request)
    DashCollectionPendenteDia = DashCollectionPendenteDiaFunction(request)
    DashCollectioAndamentoDia = DashCollectioAndamentoDiaFunction(request)
    DashCollectioConcluidoDia = DashCollectionConcluidoDiaFunction(request)
    DashProdutividadeAgendamento = DashProdutividadeAgendamentoFunction(request)
    DashProdutividadePaciente = DashProdutividadePacienteFunction(request)

    DashCollectionPendenteMes= DashCollectionPendenteMesFunction(request)
    DashCollectioAndamentoMes = DashCollectioAndamentoMesFunction(request)
    DashCollectioConcluidoMes = DashCollectionConcluidoMesFunction(request)

    PhotoRankingAtendimento_dia = PhotoRankByArrayFunction(RankingDashAtenDay)
    PhotoRankingAtendimento_mes = PhotoRankByArrayFunction(RankingDashAtenMonth)
    PhotoRankingEnfermeira_dia = PhotoRankByArrayFunction(RankingEnfermagemDay)
    PhotoRankingEnfermeira_mes = PhotoRankByArrayFunction(RankingEnfermagemMonth)


    data_ranking_atendimento_dia = _treating_data(ranking=RankingDashAtenDay, photo=PhotoRankingAtendimento_dia)
    data_ranking_atendimento_mes = _treating_data(ranking=RankingDashAtenMonth, photo=PhotoRankingAtendimento_mes)
    data_ranking_enfermeira_mes = _treating_data(ranking=RankingEnfermagemDay, photo=PhotoRankingEnfermeira_dia)
    data_ranking_enfermeira_mes = _treating_data(ranking=RankingEnfermagemMonth, photo=PhotoRankingEnfermeira_mes)

    return render(request, 'dashboards/ranking/DashService.html',
    {
        "arr_ViewFoto": ViewFoto,
        "arr_SearchRankingDashAtenDay": RankingDashAtenDay,
        "arr_SearchRankingDashAtenMonth": RankingDashAtenMonth, 
        "arr_SearchRankingEnfermagemDay": RankingEnfermagemDay, 
        "arr_SearchRankingEnfermagemMonth": RankingEnfermagemMonth, 
        "arr_DashCollectionPendenteDia": DashCollectionPendenteDia, 
        "arr_DashCollectioAndamentoDia": DashCollectioAndamentoDia, 
        "arr_DashCollectioConcluidoDia": DashCollectioConcluidoDia, 
        "arr_DashCollectionPendenteMes": DashCollectionPendenteMes, 
        "arr_DashCollectioAndamentoMes": DashCollectioAndamentoMes, 
        "arr_DashCollectioConcluidoMes": DashCollectioConcluidoMes, 
        "arr_DashProdutividadeAgendamento": DashProdutividadeAgendamento, 
        "arr_DashProdutividadePaciente": DashProdutividadePaciente,
    } 
     )


#AJUSTAR ROTA COLETA PACIENTE
#@login_required
def AdjustRouteViews(request):
    if allowPage(request, "adjust_route") == False:
        return error(request)
    ViewFoto = FilePhotoViewFunction(request)#foto perfil parte superior
    SsearchAdjustRoute =  searchAdjustRouteNurse(request)
    nurse_active = Users.objects.order_by('-data_regis').filter(status='Ativo')
    return render(request, 'manage/agenda/AdjustRoute.html', 
    
    {
        "arr_SearchAdjustRoute": SsearchAdjustRoute,
        "arr_SearchNurse": nurse_active,
        "arr_ViewFoto": ViewFoto,
    })

#API AJUSTAR ROTA
#@login_required
def ApiAdjustRoute(request):
    array = ApiAdjustRouteFunction(request)
    return JsonResponse(array, safe=False, status=200)

def ApiHistoryMyIndications(request):
    array = HistoryIndicationFunction(request)
    return JsonResponse(array, safe=False, status=200)





#teste
class ContractCollection(View):
    @staticmethod
    @login_required
    @ensure_csrf_cookie
    def get(request):
        return JsonResponse(
            ContractCollectionFunction(BodyDecode(request)),
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



def FileContract(request):
    array = FileContractFunction(request)
    return JsonResponse(array, safe=False, status=200)



def ApiHistoryPartnersViews(request):
    array = HistoricoParceiros(request)
    return JsonResponse(array, safe=False, status=200)


def Recontato_Partners(request):
    array = RecontatoFunction(request)
    return JsonResponse(array, safe=False, status=200)