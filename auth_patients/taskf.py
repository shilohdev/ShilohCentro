from __future__ import absolute_import
from celery import shared_task, Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiloh.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
appv = Celery('shiloh')
appv.config_from_object('django.conf:settings', namespace='CELERY')
CELERY_TIMEZONE = 'America/Sao_Paulo'

@appv.task
def BuscarIndicacaoSixtyDays(request):
    print("minha funcao executando")

    return True
