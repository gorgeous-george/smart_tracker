from django.urls import path

from core_app.views import CoreObjectListView, CoreObjectDetailView

urlpatterns = [
    path('', CoreObjectListView.as_view(), name='objects'),                            # page showing all objects
    path('object_details/<int:pk>', CoreObjectDetailView.as_view(), name='object_detail'),  # specific object detailed page
    ]