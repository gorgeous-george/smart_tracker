from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse

from sandbox.forms import DatasetModelForm, DatasetObjectModelForm
from dashboard.models import CoreObject, Dataset

# todo: add a Class with @login_required and @permission_required decorators for all view functions in this module
# todo: add filter to all queryset requests : Coreobject.responsible == self.request.user


def sandbox_index(request):
    """
    Base view returning all datasets and all objects,
    paginated, updated status
    """
    paginated_dataset_list = get_dataset_list(request)
    paginated_object_list = get_object_list(request)
    return render(request, 'sandbox.html', {
        'paginated_dataset_list': paginated_dataset_list,
        'paginated_object_list': paginated_object_list,
    },)


def get_dataset_list(request):
    dataset_list = Dataset.objects.all().order_by('dataset')
    paginated_dataset_list = sandbox_paginator(request, dataset_list, getparameter='dataset_page')
    return paginated_dataset_list


def get_object_list(request):
    object_list = CoreObject.objects.all().order_by('dataset', 'priority', 'current_value')
    object_list = coreobject_status_update(object_list)
    paginated_object_list = sandbox_paginator(request, object_list, getparameter='object_page')
    return paginated_object_list


def coreobject_status_update(object_list):
    """
    Object's status automatically updated based on combination of its current value and priority as per status_matrix.
    """
    status_matrix = {
        'Green': [('Green', 'Low'), ('Orange', 'Low'), ('Green', 'Moderate'), ('Green', 'High')],
        'Orange': [('Red', 'Low'), ('Orange', 'Moderate')],
        'Red': [('Red', 'Moderate'), ('Orange', 'High'), ('Red', 'High')],
    }
    for coreobject in object_list:
        if (coreobject.current_value, coreobject.priority) in status_matrix.get('Green') and coreobject.status != 'Green':
            coreobject.status = 'Green'
            coreobject.save()
        elif (coreobject.current_value, coreobject.priority) in status_matrix.get('Orange') and coreobject.status != 'Orange':
            coreobject.status = 'Orange'
            coreobject.save()
        elif (coreobject.current_value, coreobject.priority) in status_matrix.get('Red') and coreobject.status != 'Red':
            coreobject.status = 'Red'
            coreobject.save()
    return object_list


def sandbox_paginator(request, objects, getparameter):
    paginator = Paginator(objects, 5)  # Show 5 datasets/objects per page.
    page_number = request.GET.get(getparameter)
    page_obj = paginator.get_page(page_number)
    return page_obj


def dataset_show_all_objects(request):
    """
    This function returns list of all objects as response to button "Show all objects".
    """
    data = dict()
    paginated_object_list = get_object_list(request)
    data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
        'paginated_object_list': paginated_object_list,
    })
    return JsonResponse(data)


def dataset_filter_object_table(request, pk):
    """
    This function returns filtered list of dataset objects as response to button "Show objects".
    """
    data = dict()
    object_list = CoreObject.objects.filter(dataset_id=pk)
    paginated_object_list = sandbox_paginator(request, object_list, getparameter='object_page')
    data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
        'paginated_object_list': paginated_object_list,
    })
    return JsonResponse(data)


# functions below are created to handle DATASET's buttons "New dataset", "Edit", "Delete"
def save_dataset_form(request, form, template_name):
    """
    Since this function is used in more than one place, it was defined as a separate function.
    Its purpose is to validate the obtained form, save the valid form, take an updated list of all datasets,
    and return JsonResponse with the form, the updated dataset list, and the html data that will be used by ajax
    (see 'sandbox/static/assets/js/datasets.js' for details)
    """
    data = dict()
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():
            # process the data as required
            form.save()
            data['form_is_valid'] = True
            paginated_dataset_list = get_dataset_list(request)
            data['html_dataset_list'] = render_to_string('includes/partial_dataset_list.html', {
                'paginated_dataset_list': paginated_dataset_list,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def dataset_create(request):
    """
    View to handle the submitted object's creation form triggered by "New object" button.
    After the object creation it returns JsonResponse with an updated data ajax for ajax script (dataset_objects.js).
    """
    if request.method == 'POST':
        form = DatasetModelForm(request.POST)
    else:
        form = DatasetModelForm()
    return save_dataset_form(request, form, 'includes/partial_dataset_create.html')


def dataset_update(request, pk):
    """
    View to handle the submitted object's updating form triggered by "Edit" button.
    After the object updating it returns JsonResponse with an updated data for ajax script (dataset_objects.js).
    """
    dataset = get_object_or_404(Dataset, id=pk)
    if request.method == 'POST':
        form = DatasetModelForm(request.POST, instance=dataset)
    else:
        form = DatasetModelForm(instance=dataset)
    return save_dataset_form(request, form, 'includes/partial_dataset_update.html')


def dataset_delete(request, pk):
    """
    View to handle the submitted object's deletion form triggered by "Delete" button.
    After the object deletion it returns JsonResponse with an updated data for ajax script (dataset_objects.js).
    """
    dataset = get_object_or_404(Dataset, id=pk)
    data = dict()
    if request.method == 'POST':
        dataset.delete()
        data['form_is_valid'] = True
        paginated_dataset_list = get_dataset_list(request)
        data['html_dataset_list'] = render_to_string('includes/partial_dataset_list.html', {
            'paginated_dataset_list': paginated_dataset_list
        })
    else:
        context = {'dataset': dataset}
        data['html_form'] = render_to_string('includes/partial_dataset_delete.html', context, request=request)
    return JsonResponse(data)


def reload_dataset_object_table(request):
    """
    If user updates/deletes a dataset having related objects, these objects should be updated/deleted as well.
    This function returns updated list of dataset objects to reload objects table.
    todo: bug_0003 to update view for cases when only one dataset is selected, so we would need to return only this dataset's objects
    """
    data = dict()
    paginated_object_list = get_object_list(request)
    data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
        'paginated_object_list': paginated_object_list,
    })
    return JsonResponse(data)


# functions below are created to handle DATASET OBJECTS' buttons "New object", "Edit", "Delete"
def save_dataset_object_form(request, form, template_name):
    """
    This function prepares JSON data for the ajax request.
    Its purpose is to validate the obtained form, save the valid form, take an updated list of all coreobjects,
    and return JsonResponse with the form, the updated coreobject list, and the html data that will be used by ajax
    (see 'sandbox/static/assets/js/dataset_objects.js' for details)
    """
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            paginated_object_list = get_object_list(request)
            data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
                'paginated_object_list': paginated_object_list,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def dataset_object_create(request):
    """
    View to handle the submitted object's creation form triggered by "New object" button.
    After the object creation it returns JsonResponse with an updated data ajax for ajax script (dataset_objects.js).
    """
    if request.method == 'POST':
        form = DatasetObjectModelForm(request.POST)
    else:
        form = DatasetObjectModelForm()
    return save_dataset_object_form(request, form, 'includes/partial_dataset_object_create.html')


def dataset_object_update(request, pk):
    """
    View to handle the submitted object's updating form triggered by "Edit" button.
    After the object updating it returns JsonResponse with an updated data for ajax script (dataset_objects.js).
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
    After the object deletion it returns JsonResponse with an updated data for ajax script (dataset_objects.js).
    """
    coreobject = get_object_or_404(CoreObject, pk=pk)
    data = dict()
    if request.method == 'POST':
        coreobject.delete()
        data['form_is_valid'] = True
        paginated_object_list = get_object_list(request)
        data['html_dataset_object_list'] = render_to_string('includes/partial_dataset_object_list.html', {
            'paginated_object_list': paginated_object_list
        })
    else:
        context = {'coreobject': coreobject}
        data['html_form'] = render_to_string('includes/partial_dataset_object_delete.html', context, request=request)
    return JsonResponse(data)


def dataset_starter_pack(request):
    """
    Function that handles button "Starter Pack".
    Its purpose is to fill the DB with hard-coded pack of dataset and objects.
    """
    from .fixtures import starter_pack
    starter_pack.starter_datasets(request)
    starter_pack.starter_objects(request)
    messages.add_message(request, messages.SUCCESS, 'Starter pack was created')
    return HttpResponseRedirect(reverse('sandbox'))


def dataset_delete_all(request):
    """
    Function that handles button "Delete ALL".
    Its purpose is to delete all datasets and objects from the database.
    """
    Dataset.objects.all().delete()
    CoreObject.objects.all().delete()
    messages.add_message(request, messages.SUCCESS, 'Database was cleaned')
    return HttpResponseRedirect(reverse('sandbox'))
