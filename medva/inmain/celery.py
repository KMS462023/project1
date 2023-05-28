import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inmain.settings')

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = "-"
AWS_DEFAULT_REGION="ru-central1"
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')


ENDPOINT = ''

broker='sqs://{}'.format(ENDPOINT)
broker_transport_options = {
    'is_secure': True,
    'region': "ru-central1"
}

app = Celery('inmain', broker=broker)

app2 = Celery('inmain2', broker=broker)
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_transport_options = broker_transport_options

app2.config_from_object('django.conf:settings', namespace='CELERY')
app2.conf.broker_transport_options = broker_transport_options
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.enable_utc = False
app.conf.task_default_queue = 'medva_celery'

app2.autodiscover_tasks()
app2.conf.enable_utc = False
app2.conf.task_default_queue = 'medva_celery'


