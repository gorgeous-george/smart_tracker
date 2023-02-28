from django.urls import path

from dashboard.views import dashboard_index, filter_form


urlpatterns = [
    path('', dashboard_index, name='dashboard-index'),
    path('filtered/', filter_form, name='dashboard-filter')
    ]

# todo: to delete urls below, it's only for development purposes
from django.conf import settings
from dashboard.views import test

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('test/', test, name='test'),
    ]
