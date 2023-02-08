from django.urls import path

from dashboard.views import coreobject_list, coreobject_create, coreobject_update, coreobject_delete


urlpatterns = [
    path('', coreobject_list, name='coreobject-list'),
    path('objects/add/', coreobject_create, name='coreobject-add'),
    path('objects/<uuid:pk>/update/', coreobject_update, name='coreobject-update'),
    path('objects/<uuid:pk>/delete/', coreobject_delete, name='coreobject-delete'),
    ]
