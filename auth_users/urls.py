from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    #API MEU FINANCEIRO EM MASSA 
    path('create/access/all/', views.ApiCreatePermissionAll, name='ApiCreatePermissionAll'),

    #CADASTRAR USUARIO
    path('manage/cadastrar/usuarios/', views.cadastreUserViews, name='cadastreUser'),
    
    #API ATUALIZAR USUARIO INTERNO
    path('API/manage/cadastrar/usuarios/', views.ApiUpdatePerfil, name='ApiUpdatePerfil'),

    #CADASTRAR PARCEIROS
    path('manage/cadastrar/parceiros/', views.cadastrePartnesViews, name='cadastrePartnes'),
    #PRÉ PARCEIRO
    path('api/manage/cadastrar/pre-parceiros/', views.ApiCadastrePrePartners, name='ApiCadastrePrePartners'),
 
    #API CADASTRAR USER 
    path('api/manage/cadastrar/user/', views.ApiCadastreUser, name='ApiCadastreUser'),

    #API CADASTRAR PARCEIROS
    path('api/manage/cadastrar/parceiros/', views.ApiCadastrePartners, name='ApiCadastrePartners'),
    path('api/manage/cadastrar/parceiros/cancel', views.PrePartnerCancel, name='PrePartnerCancel'),

    #CADASTRAR INDICAÇÃO
    path('cadastrar/indicacao/', views.cadastreIndicationViews, name='cadastreIndication'),#LEAD
    path('ApiCadastrar/indicacao/', views.ApiCadastreIndication, name='ApiCadastreIndication'),#API CADASTRAR LEAD
    path('manage/cadastrar/paciente/', views.CadastrePatientViews, name='cadastrePatient'),#CADASTRAR PACIENTE
    path('api/cadastrar/paciente/lead', views.ApiCadastrePatientViews, name='ApiCadastrePatient'),#API CADASTRAR PACIENTE LEAD
    path('api/cadastrar/paciente/novo-registro/', views.ApiNewRegisPatient, name='ApiNewRegisPatient'),#API CADASTRAR PACIENTE NOVO REGISTRO
    

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
    #AJUSTAR ROTA COLETA PACIENTE
    path('consultar/coletas/ajustar/rota', views.AdjustRouteViews, name='AdjustRouteViews'),#AJUSTAR ROTA DE AGENDAMENTOS
    path('api/consultar/coletas/ajustar/rota', views.ApiAdjustRoute, name='ApiAdjustRoute'), #API AJUSTAR ROTA

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
    path('api/consultar/coletas/modal', views.ApiScheduledPickupModalViews, name='ApiScheduledPickupModal'),#API MODAL AGENDAMENTO

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
    path('api/modal/parceiros/int', views.ApiViewDataPartnersModalint, name='ApiViewDataPartnersModalint'), #Meeus parceiros


 
    #LISTAR PACIENTES
    path('listar/pacientes/', views.listIndicationViews, name='listIndication'),
    path('api/modal/pacientes/', views.ApiViewDataPatientsModal, name='ApiViewDataPatientsModal'),
    path('api/modal/pacientes/update', views.ApiChangePatientsModal, name='ApiChangePatientsModal'), #UPDATE PACIENTE
    path('api/modal/pacientes/files', views.FetchPatientsFiles.as_view(), name='FetchPatientsFiles'), #FILE PACIENTE
    
    #LISTAR TODOS OS LEADS
    path('listar/leads/', views.listLeadsViews, name='listLeads'),
    path('listar/leads/status', views.ApiStatusNegative, name='ApiStatusNegative'),
 

    #FINANCEIRO EXAMES
    #AGENDAMENTOS CONCLUIDOS
    path('financeiro/exames/process/', views.FinancialExamsViews, name='FinancialExamsViews'), #FINANCEIRO EXAMES
    path('api/financeiro/exames/process/files/remove/', views.ModalExamsFinanceFileRemove, name='ModalExamsFinanceFileRemove'), #FINANCEIRO EXAMES
    path('api/financeiro/exames/process/files/remove/int', views.ModalExamsFinanceFileRemoveInt, name='ModalExamsFinanceFileRemoveInt'), #FINANCEIRO EXAMES

    path('Api/financeiro/exames/start/process/', views.ApiStartProcess, name='ApiStartProcess'), #FINANCEIRO
    path('api/consultar/exames/modal', views.SearchModalExams, name='SearchModalExams'),#API MODAL AGENDAMENTO
    path('api/consultar/exames/modal/finances', views.SearchModalExamsFinances, name='SearchModalExamsFinances'),#API MODAL FINANCEIRO
    path('api/salvar/alteracoes/modal/finances', views.SaveEditionsFinances, name='SaveEditionsFinances'),#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
    path('api/finalizar/exames/modal/', views.ApiFinalizeProcess, name='ApiFinalizeProcess'),#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
    path('financeiro/search/exames/solicitacoes/', views.SearchMonthExamsRefund, name='SearchMonthExamsRefund'),#EXAMES FINALIZADOS
    #PAGAMENTOS PAREIROS 
    path('financeiro/fechamento/parceiros/', views.ClosingPartnersViews, name='ClosingPartners'),#EXAMES FINALIZADOS
    path('financeiro/fechamento/parceiros/filter', views.SearchMonthClosingPartners, name='SearchMonthClosingPartners'),#EXAMES FINALIZADOS
    path('financeiro/fechamento/parceiros/detalhes', views.paymentDetails, name='paymentDetails'),
    path('financeiro/fechamento/parceiros/pay', views.payPartnersV, name='payPartnersV'),
    path('financeiro/modal/parceiros/status', views.SearchInfoM, name='SearchInfoM'),
    #PAGAMENTOS COMERCIAL
    path('financeiro/modal/comercial/', views.ClosingCommercialViews, name='ClosingCommercial'),#EXAMES FINALIZADOS
    path('financeiro/fechamento/comercial/filter', views.SearchMonthClosingCommercial, name='SearchMonthClosingCommercial'),#EXAMES FINALIZADOS
    path('financeiro/fechamento/comercial/detalhes', views.paymentDetailsCommercial, name='paymentDetailsCommercial'),
    path('financeiro/modal/comercial/status/', views.SearchInfoCommercial, name='SearchInfoCommercial'),
    path('financeiro/fechamento/parceiros/detalhes', views.payCommercial, name='payCommercial'),



    #FINALIZADOS
    path('financeiro/exames/exames/process-fin/', views.RefundCompletedViews, name='RefundCompletedViews'),#EXAMES FINALIZADOS
    path('financeiro/search/exames/finish/', views.SearchMonthExamsConcl, name='SearchMonthExamsConcl'),#EXAMES FINALIZADOS
    #path('api/historico/actions/', views.HistoricoViews, name='HistoricoViews'),#API HISTÓRICO
    #NÃO ATINGIDO
    path('financeiro/reembolso/nao/atingido/', views.refundNotReachedViews, name='refundNotReachedViews'),
    #GLOSADO
    path('financeiro/reembolso/glosado/', views.refundGlossesViews, name='refundGlossesViews'),

    #INDIVIDUAL, MEUS REGISTROS
    path('listar/pacientes/meus-registros/', views.ListerPatientsUnitViews, name='ListerPatientsUnitViews'),#PACIENTES
    path('listar/parceiros/meus-registros/', views.ListerPartnersUnitViews, name='ListerPartnersUnitViews'),#PARCEIROS
    path('listar/indicacoes/meus-registros/', views.ListerIndicationsUnitViews, name='ListerIndicationsUnitViews'),#INDICAÇÕES
    path('api/indicacoes/meus-registros/', views.ApiHistoryMyIndications, name='ApiHistoryMyIndications'),#INDICAÇÕES
    path('meu/fechamento/financeiro/', views.ClosingFinanceUnit, name='ClosingFinanceUnit'),#INDICAÇÕES
    path('api/meus/parceiros/atualizacao/', views.ApiAttPartners, name='ApiAttPartners'),#INDICAÇÕES
    
    #MEU PERFIL
    path('meu/perfil/', views.MyProfileViews, name='myProfile'),
    #API MEU PERFIL
    path('api/meu/perfil/salvar/', views.ApichangeUserProfile, name='ApichangeUserProfile'), 

 

    #LISTAR LEADS
    path('listar/leads/all-leads/', views.LeadsViews, name='LeadsViews'),#INDICAÇÕES
    path('listar/leads/all-leads/filtro', views.SearchStatusLeadFilter, name='SearchStatusLeadFilter'),#EXAMES FINALIZADOS

    
    #CADASTRAR LEAD (INTERNO)
    path('cadastrar/leads/interno/', views.CadatsreLeadViews, name='CadatsreLeadViews'),#INDICAÇÕES CADASTRADAS PELO ATENDIMENTO
    path('api/cadastrar/leads/interno/', views.ApiCadatsreLeadViews, name='ApiCadatsreLeadViews'),


    #CADASTRAR UNIDADE
    path('manage/cadastrar/unidade/', views.cadastreUnitViews, name='cadastreUnit'),

    #API CADASTRAR CONVENIO
    path('api/cadastre/unidade', views.ApiCadastreUnit, name='ApiCadastreUnit'),
    path('api/unit/status/change/', views.ApiChangeStatusUnit, name='ApiChangeStatusUnit'),

    #SALVAR ANEXO PACIENTES - listar paciente
    path('api/salvar/doc/paciente', views.SaveEditionsPatient, name='SaveEditionsPatient'),

    #PROCEDIMENTO INERTNO 
    #AGENDAR COLETA 
    path('agendaar/coleta/interna/', views.schedulePickupIntViews, name='schedulePickupInt'),#EXAMES FINALIZADOS
    #API AGENDAR COLETA
    path('api/agendar/coleta/paciente/interna/', views.ApiSchedulePickupIntViews, name='ApiSchedulePickupInt'),
    #CONSULTAR COLETAS AGENDADAS
    path('consultar/coletas/internas/', views.ScheduledPickupIntViews, name='ScheduledPickupInt'),#RENDER PAGE
    path('consultar/coletas/internas/int', views.ScheduledMonthIntViews, name='ScheduledMonthIntViews'),#FILTRO MES 
    path('api/status/agenda/int', views.ApiStatusAgendaConcInt, name='ApiStatusAgendaConcInt'),#CONCLUIR
    path('api/consultar/coletas/modal/interno/', views.ApiScheduledPickupModalIntViews, name='ApiScheduledPickupModalInt'),#API MODAL AGENDAMENTO
    path('financeiro/search/exames/solicitacoes/interno/', views.SearchMonthExamsSolicitationViews, name='SearchMonthExamsSolicitationViews'),#EXAMES FINALIZADOS

    #FINANCEIRO INTERNO
    #AGENDAMENTOS CONCLUIDOS
    path('financeiro/solicitacoes/interna/', views.SolicitationsRetfund, name='SolicitationsRetfund'), #FINANCEIRO EXAMES
    path('financeiro/exames/exames/filter/', views.SearchMonthFInalizadosInt, name='SearchMonthFInalizadosInt'),#EXAMES FINALIZADOS

    #FINALIZADOS
    path('financeiro/exames/exames/process-fin/interno/', views.RefundCompletedInternoViews, name='RefundCompletedInterno'),#EXAMES FINALIZADOS
    path('financeiro/exames/exames/filter/', views.SearchMonthFInalizadosInt, name='SearchMonthFInalizadosInt'),#EXAMES FINALIZADOS


    #ENFERMEIROS
    path('rota/agendamentos/coletas/', views.CollectionRouteViews, name='CollectionRouteViews'),#EXAMES FINALIZADOS
    path('api/status/agenda/route', views.ApiIniciarColeta, name='ApiIniciarColeta'),#CONCLUIR
    path('api/salvar/anexo/', views.SaveAnexo, name='SaveAnexo'),#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
    path('fechamento/finacneiro/interno/', views.closingInt, name='closingInt'),#SALVAR ALTERAÇÕES MODAL FINANCEIRO EXAME
    path('financeiro/fechamento/interno/filter', views.SearchClosingIntFilter, name='SearchClosingIntFilter'),#EXAMES FINALIZADOS

    #INFOLOG
    path('info/log/', views.LogUser, name='LogUser'),#EXAMES FINALIZADOS

 
    
    #API PARTNERSS
    path('anx/nf/partners/', views.ApiNfPartners, name='ApiNfPartners'),#EXAMES FINALIZADOS
    path('anx/nf/partners/ger-file/', views.ApiGerFilePartners, name='ApiGerFilePartners'),#EXAMES FINALIZADOS
    path('api/modal/parceiros/files', views.FetchPartnersFiles.as_view(), name='FetchPartnersFiles'), #FILE PACIENTE
    path('api/financeiro/pagamentos/partners/files/remove', views.RemoveFilePartners, name='RemoveFilePartners'), #FINANCEIRO EXAMES


    #DASBOARDS
    path('dashboards/financeiro/reembolsos/', views.DashboardsRefunds, name='DashboardsRefunds'), #FINANCEIRO EXAMES
    #path('dashboard/ranking/coletas/', views.DashCollectionsViews, name='DashCollections'),# TELA DE COLETAS
    path('dashboard/ranking/comercial/', views.DashCommercialViews, name='DashCommercial'),#RANKING COMERCIAL
    path('dashboard/ranking/atendimento/', views.DashServiceViews, name='DashService'),#RANKING ATENDIMENTO

    #ANEXAR ARQUIVO FINANCEIRO
    path('api/anx/docs/', views.ApiAnexarFiles, name='ApiAnexarFiles'), # ANEXAR FILES
        
    
    #ANEXAR FOTO MEU PERFIL
    path('api/anx/foto-perfil/', views.ApiPhotoProfile, name='ApiPhotoProfile'), #FINANCEIRO EXAMES
    path('api/preview/file/foto-perfil/', views.FilePhotoView, name='FilePhotoView'), #FILE PACIENTE


    #teste
    path('api/contrato/coleta/', views.ContractCollection.as_view(), name='ContractCollection'), #FILE PACIENTE


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  