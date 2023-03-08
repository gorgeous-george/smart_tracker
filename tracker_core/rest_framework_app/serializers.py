from dashboard.models import Dataset, CoreObject
from django.contrib.auth import get_user_model
from rest_framework import serializers

"""
Currently active user model is imported for representing clients. 
This method will return default django User model or the custom user model if one would be specified.
"""
User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'last_login',
            'is_superuser',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
        ]


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'dataset',
            'description',
            'owner',
        ]


class CoreObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoreObject
        fields = [
            'id',
            'name',
            'description',
            'dataset',
            'current_value',
            'priority',
            'measure_description',
            'status',
            'timeframe',
            'responsible',
        ]
