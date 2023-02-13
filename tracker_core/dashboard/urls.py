from django.urls import path

from dashboard.views import coreobject_list


urlpatterns = [
    path('', coreobject_list, name='coreobject-list'),
    ]
