from django import forms
from django.core.exceptions import ValidationError

from dashboard.models import CoreObject, Dataset


class DatasetModelForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = [
            "dataset",
            "description",
            "owner"
        ]


class DatasetObjectModelForm(forms.ModelForm):

    class Meta:
        model = CoreObject
        fields = [
            "name",
            "description",
            "dataset",
            "measure",
            "measure_limit",
            "measure_description",
            "timeframe",
            "responsible",
        ]

    """
    template for custom validation
    """
    # def clean_description(self):
    #     data = self.cleaned_data['description']
    #     if "fred@example.com" not in data:
    #         raise ValidationError("You have forgotten about Fred!")
    #
    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
    #     return data