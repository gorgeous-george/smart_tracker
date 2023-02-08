from django.urls import path

from sandbox.views import create_dataset, sandbox_index


urlpatterns = [
    path('', sandbox_index, name='sandbox'),
    path('datasets/create/', create_dataset, name='dataset-add'),
    ]
