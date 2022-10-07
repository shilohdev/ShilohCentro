from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from auth_patients.taskf import BuscarIndicacaoSixtyDays


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shiloh.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('shiloh')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # ROTINA
    sender.add_periodic_task(10, BuscarIndicacaoSixtyDays.s(True), name='Verificar indicação a cada 60 dias')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()
