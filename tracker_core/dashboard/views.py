from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from dashboard.models import CoreObject, Dataset
from dashboard.forms import CoreObjectModelForm


def index(request):
    """
    Base view function for the home page.
    """
    return render(request, 'index.html')


def test(request):
    """
    todo: to delete this view function, it has been created only for testing
    """
    return render(request, 'test.html')


def coreobject_paginator(request, coreobjects):
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


def get_data_for_chart(coreobjects):
    chart_data = [['Status', 'Count']]
    green_count = len(coreobjects.filter(status='G'))
    orange_count = len(coreobjects.filter(status='O'))
    red_count = len(coreobjects.filter(status='R'))
    chart_data += ['Red', red_count], ['Orange', orange_count], ['Green', green_count]
    return chart_data


def coreobject_list(request):
    """
    View representing application's main page.
    Its default purpose is to return a paginated and filtered queryset of all coreobjects.
    """
    coreobjects = CoreObject.objects.all()
    page_obj = coreobject_paginator(request, coreobjects)
    chart_data = get_data_for_chart(coreobjects)
    unique_obj_types = get_unique_datasets()
    return render(request, 'coreobject_list.html', {
        'page_obj': page_obj,
        'chart_data': chart_data,
        'unique_obj_types': unique_obj_types,
    })


def save_coreobject_form(request, form, template_name):
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
            page_obj = coreobject_paginator(request, coreobjects)
            data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
                'page_obj': page_obj,
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def coreobject_create(request):
    """
    View to handle the submitted object's creation form triggered by "New object" button.
    After the object creation it returns JsonResponse with an updated data ajax for ajax script (coreobjects.js).
    """
    if request.method == 'POST':
        form = CoreObjectModelForm(request.POST)
    else:
        form = CoreObjectModelForm()
    return save_coreobject_form(request, form, 'includes/partial_coreobject_create.html')


def coreobject_update(request, pk):
    """
    View to handle the submitted object's updating form triggered by "Edit" button.
    After the object updating it returns JsonResponse with an updated data for ajax script (coreobjects.js).
    """
    coreobject = get_object_or_404(CoreObject, pk=pk)
    if request.method == 'POST':
        form = CoreObjectModelForm(request.POST, instance=coreobject)
    else:
        form = CoreObjectModelForm(instance=coreobject)
    return save_coreobject_form(request, form, 'includes/partial_coreobject_update.html')


def coreobject_delete(request, pk):
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
        data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
            'page_obj': page_obj
        })
    else:
        context = {'coreobject': coreobject}
        data['html_form'] = render_to_string('includes/partial_coreobject_delete.html', context, request=request)
    return JsonResponse(data)


def coreobject_filter(request, value):
    """
    View to handle a received obj_type submitted by "Filter" button.
    It returns JsonResponse with filtered queryset for ajax script that reloads the coreobject list table.
    """
    queryset = get_list_or_404(CoreObject, obj_type=value).values()
    data = dict()
    page_obj = queryset
    data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
        'page_obj': page_obj
    })
    return JsonResponse(data)


def get_unique_datasets():
    unique_datasets = Dataset.objects.values_list('dataset')
    return unique_datasets



