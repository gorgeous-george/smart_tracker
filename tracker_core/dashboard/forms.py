from django import forms
from django.forms import CheckboxSelectMultiple, SelectMultiple

from dashboard.models import Dataset

qs = Dataset.objects.all()
dataset_choices = [('*', 'All')]
for dataset in qs:
    dataset_choices.append((str(dataset.id), str(dataset.dataset)))

status_choices = [
    ('*', 'All'),
    ('Red', 'Red'),
    ('Orange', 'Orange'),
    ('Green', 'Green'),
]

priority_choices = [
    ('*', 'All'),
    ('High', 'High'),
    ('Moderate', 'Moderate'),
    ('Low', 'Low'),
]

timeframe_choices = [
    ('*', 'All'),
    ('Day', 'Day'),
    ('Week', 'Week'),
    ('Month', 'Month'),
    ('Year', 'Year'),
]


class TestForm(forms.Form):
    # todo: to delete TestForm, it's only for development purposes
    datasets = forms.MultipleChoiceField(
        choices=dataset_choices,
        widget=SelectMultiple(attrs={'class': 'form-select'}
                              ),
        initial='*',
    )
    status = forms.MultipleChoiceField(
        choices=status_choices,
        required=False,
        widget=CheckboxSelectMultiple(attrs={}),
        initial='*',
    )


class DashboardFilterForm(forms.Form):
    datasets = forms.MultipleChoiceField(
        choices=dataset_choices,
        required=True,
        widget=SelectMultiple(attrs={'class': 'form-select', 'style': 'width:100%', 'size': 6}),
        initial='*',
    )
    status = forms.MultipleChoiceField(
        choices=status_choices,
        required=False,
        widget=CheckboxSelectMultiple(attrs={}),
        initial='*',
    )
    priority = forms.MultipleChoiceField(
        choices=priority_choices,
        required=False,
        widget=CheckboxSelectMultiple(attrs={}),
        initial='*',
    )
    timeframe = forms.MultipleChoiceField(
        choices=timeframe_choices,
        required=False,
        widget=CheckboxSelectMultiple(attrs={}),
        initial='*',
    )
