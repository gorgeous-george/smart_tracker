from django.urls import path

from core_app.views import coreobject_list, coreobject_create, coreobject_update, coreobject_delete, tutorial
from sandbox.views import sandbox


urlpatterns = [
    path('objects/', coreobject_list, name='coreobject-list'),
    path('objects/add/', coreobject_create, name='coreobject-add'),
    path('objects/<uuid:pk>/update/', coreobject_update, name='coreobject-update'),
    path('objects/<uuid:pk>/delete/', coreobject_delete, name='coreobject-delete'),
    path('tutorial/', tutorial, name='tutorial'),
    path('sandbox/', sandbox, name='sandbox'),
    ]
