from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from sandbox.forms import DatasetForm
from dashboard.models import Dataset


def sandbox_index(request):
    dataset_list = get_dataset_list()
    return render(request, 'sandbox.html',
                  {'dataset_list': dataset_list},
                  )


def get_dataset_list():
    dataset_list = Dataset.objects.all()
    return dataset_list


def dataset_create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DatasetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            dataset = form.cleaned_data['dataset']
            description = form.cleaned_data['description']
            Dataset.objects.create(
                dataset=dataset,
                description=description,
            )
            messages.success(request, f"Dataset '{dataset}' was created.")
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('sandbox'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DatasetForm()
    return render(request, 'sandbox.html', {'form': form})


def dataset_update(request, pk):
    return render(request, 'sandbox.html')


def dataset_delete(request, pk):
    return render(request, 'sandbox.html')
