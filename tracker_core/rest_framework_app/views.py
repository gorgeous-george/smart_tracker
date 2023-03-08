from dashboard.models import Dataset, CoreObject
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import mixins, status, viewsets, permissions

from rest_framework_app.serializers import DatasetSerializer, CoreObjectSerializer, UserSerializer

"""
Currently active user model is imported for representing clients. 
This method will return default django User model or the custom user model if one would be specified.
"""
User = get_user_model()


class ReadOnlyUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed.
    It provides only `list()` and `retrieve()` actions.
    """

    # Disable the create, update, partial update and delete actions
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DatasetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]


class CoreObjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CoreObject.objects.all()
    serializer_class = CoreObjectSerializer
    permission_classes = [permissions.IsAuthenticated]
