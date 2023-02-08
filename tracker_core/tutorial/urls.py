from django.urls import path

from tutorial.views import tutorial

urlpatterns = [
    path('', tutorial, name='tutorial'),
    ]
