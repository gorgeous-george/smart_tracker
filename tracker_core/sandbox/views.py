from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse

from sandbox.forms import DatasetForm, DatasetObjectModelForm
from dashboard.models import CoreObject, Dataset


def sandbox_index(request):
    """
    base view returning all datasets and all objects
    todo: to add "if filtered - filter , else all"
    """
    dataset_list = get_dataset_list()
    objects_list = get_all_objects(request)
    return render(request, 'sandbox.html', {
        'dataset_list': dataset_list,
        'page_obj': objects_list,
    },)


def get_dataset_list():
    dataset_list = Dataset.objects.all()
    return dataset_list


def get_dataset_objects(dataset):
    dataset_objects = get_list_or_404(CoreObject, dataset=dataset)
    return dataset_objects


def get_all_objects(request):
    """
    To return a paginated queryset of all coreobjects.
    """
    coreobjects = CoreObject.objects.all()
    page_obj = dataset_object_paginator(request, coreobjects)
    return page_obj


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


def dataset_object_paginator(request, coreobjects):
    """
    Since paginator is used in more than one place, it was defined as a separate function.
    It is called by:
    - coreobject_list()
    - save_coreobject_form()
    """
    paginator = Paginator(coreobjects, 10)  # Show 10 coreobjects per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj





def save_dataset_object_form(request, form, template_name):
    """
    Since this function is used in more than one place, it was defined as a separate function.
    Its purpose is to validate the obtained form, save the valid form, take an updated list of all coreobjects,
    and return JsonResponse with the form, the updated coreobject list and the html for templates update that
     will be used by ajax (see 'static/assets/js/coreobjects.js' for details)
    It is called by:
    - coreobject_create()
    - coreobject_update()
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            coreobjects = CoreObject.objects.all()
            page_obj = dataset_object_paginator(request, coreobjects)
            data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
                'page_obj': page_obj,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def dataset_object_create(request):
    """
    View to handle the submitted object's creation form triggered by "New object" button.
    After the object creation it returns JsonResponse with an updated data ajax for ajax script (coreobjects.js).
    """
    if request.method == 'POST':
        form = DatasetObjectModelForm(request.POST)
    else:
        form = DatasetObjectModelForm()
    return save_dataset_object_form(request, form, 'includes/partial_dataset_object_create.html')


def dataset_object_update(request, pk):
    """
    View to handle the submitted object's updating form triggered by "Edit" button.
    After the object updating it returns JsonResponse with an updated data for ajax script (coreobjects.js).
    """
    coreobject = get_object_or_404(CoreObject, pk=pk)
    if request.method == 'POST':
        form = DatasetObjectModelForm(request.POST, instance=coreobject)
    else:
        form = DatasetObjectModelForm(instance=coreobject)
    return save_dataset_object_form(request, form, 'includes/partial_dataset_object_update.html')


def dataset_object_delete(request, pk):
    """
    View to handle the submitted object's deletion form triggered by "Delete" button.
    After the object deletion it returns JsonResponse with an updated data for ajax script (coreobjects.js).
    """
    coreobject = get_object_or_404(CoreObject, pk=pk)
    data = dict()
    if request.method == 'POST':
        coreobject.delete()
        data['form_is_valid'] = True
        page_obj = CoreObject.objects.all()
        data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
            'page_obj': page_obj
        })
    else:
        context = {'coreobject': coreobject}
        data['html_form'] = render_to_string('includes/partial_dataset_object_delete.html', context, request=request)
    return JsonResponse(data)
