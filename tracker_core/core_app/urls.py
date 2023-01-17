from django.urls import path

from core_app.views import (
    CoreObjectCreateView,
    CoreObjectDeleteView,
    CoreObjectListView,
    CoreObjectDetailView,
    CoreObjectUpdateView,
)

urlpatterns = [
    path('object/list', CoreObjectListView.as_view(), name='coreobject-list'),
    path('object/<uuid:pk>', CoreObjectDetailView.as_view(), name='coreobject-detail'),
    path('object/add/', CoreObjectCreateView.as_view(), name='coreobject-add'),
    path('object/<uuid:pk>/', CoreObjectUpdateView.as_view(), name='coreobject-update'),
    path('object/<uuid:pk>/delete/', CoreObjectDeleteView.as_view(), name='coreobject-delete'),
    ]
