from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# Django'nun default ayarlarını celery'e tanıt
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmployeeTrackingSystem.settings')

app = Celery('EmployeeTrackingSystem')

# Celery, Django ayarlarından 'CELERY' ile başlayanları otomatik olarak alır
app.config_from_object('django.conf:settings', namespace='CELERY')

# Görevlerin otomatik olarak bulunmasını sağla
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

