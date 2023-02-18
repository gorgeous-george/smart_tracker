from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from django.http import JsonResponse
from django.template.loader import render_to_string

from dashboard.models import CoreObject, Dataset


# todo: add a Class with @login_required and @permission_required decorators for all view functions in this module
# todo: show user only his/her dataset/objects : Coreobject.responsible = Dataset.owner = self.request.user


def index(request):
    """
    Base view function for the home page.
    """
    return render(request, 'index.html')


def coreobject_list(request):
    """
    To return a paginated and filtered queryset of all coreobjects.
    """
    coreobjects = CoreObject.objects.all()
    page_obj = coreobject_paginator(request, coreobjects)
    chart_data = get_data_for_chart(coreobjects)
    unique_dataset_names = Dataset.objects.all()
    return render(request, 'coreobject_list.html', {
        'page_obj': page_obj,
        'chart_data': chart_data,
        'unique_dataset_names': unique_dataset_names,
    })


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
    green_count = len(coreobjects.filter(status='Green'))
    orange_count = len(coreobjects.filter(status='Orange'))
    red_count = len(coreobjects.filter(status='Red'))
    chart_data += ['Red', red_count], ['Orange', orange_count], ['Green', green_count]
    return chart_data


def coreobject_filter(request, value):
    """
    View to handle a received obj_type submitted by "Filter" button.
    It returns JsonResponse with filtered queryset for ajax script that reloads the coreobject list table.
    """
    queryset = get_list_or_404(CoreObject, dataset=value)
    data = dict()
    page_obj = queryset
    data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
        'page_obj': page_obj
    })
    return JsonResponse(data)




