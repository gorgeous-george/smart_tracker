from django.urls import path

from sandbox.views import dataset_create, dataset_delete, dataset_update, sandbox_index


urlpatterns = [
    path('', sandbox_index, name='sandbox'),
    path('datasets/create/', dataset_create, name='dataset-add'),
    path('datasets/<int:pk>/update/', dataset_update, name='dataset-update'),
    path('datasets/<int:pk>/delete/', dataset_delete, name='dataset-delete'),
    ]
