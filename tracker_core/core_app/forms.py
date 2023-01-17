from django import forms
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
