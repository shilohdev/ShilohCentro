from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #CADASTRAR USUARIO
    path('manage/cadastrar/usuarios/', views.cadastreUserViews, name='cadastreUser'),

    #CADASTRAR PARCEIROS
    path('manage/cadastrar/parceiros/', views.cadastrePartnesViews, name='cadastrePartnes'),
 
    #API CADASTRAR USER 
    path('api/manage/cadastrar/user/', views.ApiCadastreUser, name='ApiCadastreUser'),

    #CADASTRAR PARCEIROS
    path('api/manage/cadastrar/parceiros/', views.ApiCadastrePartners, name='ApiCadastrePartnes'),

    #CADASTRAR INDICAÇÃO
    path('cadastrar/indicacao/', views.cadastreIndicationViews, name='cadastreIndication'),#LEAD
    path('ApiCadastrar/indicacao/', views.ApiCadastreIndication, name='ApiCadastreIndication'),#API CADASTRAR LEAD
    path('manage/cadastrar/paciente/', views.CadastrePatientViews, name='cadastrePatient'),#CADASTRAR PACIENTE
    path('api/cadastrar/paciente/', views.ApiCadastrePatientViews, name='ApiCadastrePatient'),#API CADASTRAR PACIENTE

    #API FORMATAR CPF
    path('api/cpf/', views.apiFormatCPF, name='apiFormatCPF'),
    
    #API FORMATAR CPF
    path('api/tel/', views.apiFormatTEL, name='apiFormatTEL'),

    #CADASTRAR CONVENIO
    path('manage/cadastrar/convenio/', views.cadastreConvenioViews, name='cadastreConvenio'),

    #API CADASTRAR CONVENIO
    path('api/cadastre/convenio', views.ApiCadastreConvenio, name='ApiCadastreConvenio'),
    path('api/convenio/status/change/', views.ApiChangeStatusConvenio, name='ApiChangeStatusConvenio'),
    
    #API PERMISSOES USERS 
    path('api/permissions/users', views.ApiPermissionsUsers, name='ApiPermissionsUsers'),

    #AGENDAR COLETA
    path('agendar/coleta/paciente', views.schedulePickupViews, name='schedulePickup'),

    #API AGENDAR COLETA
    path('api/agendar/coleta/paciente', views.ApiSchedulePickupViews, name='ApiSchedulePickup'),
    

    #CONSULTAR COLETAS AGENDADAS
    path('consultar/coletas/paciente', views.ScheduledPickupViews, name='ScheduledPickup'),
    path('api/status/agenda', views.ApiStatusAgendaConc, name='ApiStatusAgendaConc'),#CONCLUIR
    path('api/coletas/reagendar/', views.ApiReagendarAgendaConc, name='ApiReagendarAgendaConc'),#REAGENDAR
    path('api/status/frustrar', views.ApiStatusAgendaFrustrado, name='ApiStatusAgendaFrustrado'),#FRUSTAR
    path('api/status/cancelar', views.ApiStatusAgendaCancel, name='ApiStatusAgendaCancel'),#CANCELAR
    #path('api/status/select/status', views.SelectFunctionStatusSelect, name='SelectFunctionStatusSelect'),#STATUS


    #API CONSULTAR COLETA
    path('api/consultar/coletas/paciente', views.ApiScheduledPickupViews, name='ApiScheduledPickup'),
    path('api/consultar/coletas/modal', views.ApiScheduledPickupModalViews, name='ApiScheduledPickupModal'),#API MODAL AGENDAMENTP


    #LISTAR USUARIOS
    path('listar/usuarios/', views.listUsersViews, name='listUsers'),
    path('api/listar/usuarios/', views.ApiListUsersViews, name='ApiListUsers'), #API LISTAR SELECT
    path('api/modal/usuarios/', views.ApiViewDataUserModal, name='ApiViewDataUserModal'),#API MODAL USUARIO
    path('api/user/status/change/', views.ApiChangeStatus, name='ApiChangeStatus'),
    path('api/user/dados/atualizar/', views.ApiChangeUsersModal, name='ApiChangeUsersModal'),
    
    #LISTAR PARCEIROS
    path('listar/parceiros/', views.listPartnesViews, name='listPartnes'),
  
    #API LISTAR PARCEIROS 
    path('api/listar/parceiros/', views.ApiListPartnesViews, name='ApiListPartnes'),
    path('api/modal/parceiros/', views.ApiViewDataPartnersModal, name='ApiViewDataPartnersModal'),


    #LISTAR PACIENTES
    path('listar/indicacao/', views.listIndicationViews, name='listIndication'),
    path('api/modal/pacientes/', views.ApiViewDataPatientsModal, name='ApiViewDataPatientsModal'),
    path('api/modal/pacientes/update', views.ApiChangePatientsModal, name='ApiChangePatientsModal'), #UPDATE PACIENTE
    
    #LISTAR LEAD
    path('listar/leads/', views.listLeadsViews, name='listLeads'),


#FINANCEIRO EXAMES
    #AGENDAMENTOS CONCLUIDOS
    path('financeiro/exames/process-int/', views.FinancialExamsViews, name='FinancialExamsViews'), #FINANCEIRO EXAMES
    path('Api/financeiro/exames/start/process/', views.ApiStartProcess, name='ApiStartProcess'), #FINANCEIRO
    path('api/consultar/exames/modal', views.SearchModalExams, name='SearchModalExams'),#API MODAL AGENDAMENTO
    path('api/consultar/exames/modal/finances', views.SearchModalExamsFinances, name='SearchModalExamsFinances'),#API MODAL FINANCEIRO
    path('api/salvar/alteracoes/modal/finances', views.SaveEditionsFinances, name='SaveEditionsFinances'),#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
    path('api/finalizar/exames/modal/', views.ApiFinalizeProcess, name='ApiFinalizeProcess'),#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
    #FINALIZADOS
    path('financeiro/exames/exames/process-fin/', views.RefundCompletedViews, name='RefundCompletedViews'),#EXAMES FINALIADOS
    path('financeiro/search/exames/finish/', views.SearchMonthExamsConcl, name='SearchMonthExamsConcl'),#EXAMES FINALIADOS


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 