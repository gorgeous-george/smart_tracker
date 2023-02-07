from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from sandbox.forms import DatasetForm
from core_app.models import Dataset


def sandbox(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DatasetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Dataset.objects.create(
                dataset=form.cleaned_data['dataset'],
                description=form.cleaned_data['description'],
            )
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('sandbox'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DatasetForm()
    return render(request, 'sandbox.html', {'form': form})
