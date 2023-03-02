from django.urls import path

from sandbox.views import (
    sandbox_index,
    dataset_create,
    dataset_delete,
    dataset_update,
    dataset_object_create,
    dataset_object_update,
    dataset_object_delete,
    reload_dataset_object_table,
    dataset_delete_all,
    dataset_filter_object_table,
    dataset_show_all_objects,
    dataset_starter_pack,
)


urlpatterns = [
    path('', sandbox_index, name='sandbox'),
    path('datasets/add/', dataset_create, name='dataset-add'),
    path('datasets/starter_pack/', dataset_starter_pack, name='dataset-starter-pack'),
    path('datasets/delete_all/', dataset_delete_all, name='dataset-delete-all'),
    path('datasets/<int:pk>/update/', dataset_update, name='dataset-update'),
    path('datasets/<int:pk>/delete/', dataset_delete, name='dataset-delete'),
    path('objects/add/', dataset_object_create, name='dataset-object-add'),
    path('objects/<uuid:pk>/update/', dataset_object_update, name='dataset-object-update'),
    path('objects/<uuid:pk>/delete/', dataset_object_delete, name='dataset-object-delete'),
    path('objects/reload/', reload_dataset_object_table, name='dataset-object-reload'),
    path('objects/all/', dataset_show_all_objects, name='dataset-object-all'),
    path('datasets/<int:pk>/filter/', dataset_filter_object_table, name='dataset-object-filter'),
    ]
