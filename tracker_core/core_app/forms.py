from django import forms
from django.core.exceptions import ValidationError

from core_app.models import CoreObject


class CoreObjectModelForm(forms.ModelForm):

    class Meta:
        model = CoreObject
        fields = [
            "name",
            "description",
            "obj_type",
            "measure",
            "_measure_limit",
            "measure_unit",
            "status",
            "lifelong_period",
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