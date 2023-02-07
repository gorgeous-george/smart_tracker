from django import forms


class DatasetForm(forms.Form):
    dataset = forms.CharField(label='dataset_name', max_length=100)
    description = forms.CharField(label='dataset_description', max_length=100)
