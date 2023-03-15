import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# prod settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_docker_prod")
# dev settings - only for development
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_local_sqlite_non-docker")

from django.conf import settings  # noqa

app = Celery("tracker_core")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY_")
app.autodiscover_tasks()
