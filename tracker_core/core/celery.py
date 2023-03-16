import os

from celery import Celery

from celery.schedules import crontab

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


# schedule of periodic tasks
app.conf.beat_schedule = {
    # Digest email. Executes every Monday morning at 7:30 a.m.
    'digest-monday-morning': {
        'task': 'dashboard.tasks.digest',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (),
    },
    # Daily mail. Executes daily at 7:30 a.m.
    'daily-morning': {
        'task': 'dashboard.tasks.daily_review_reminder',
        'schedule': crontab(hour=7, minute=30, day_of_week='*'),
        'args': (),
    },
    # test task
    'test': {
        'task': 'dashboard.tasks.test',
        'schedule': crontab(),
        'args': (),
    },
}
