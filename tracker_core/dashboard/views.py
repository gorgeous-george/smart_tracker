from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from dashboard.models import CoreObject
from dashboard.forms import DashboardFilterForm

# todo: add a Class with @login_required and @permission_required decorators for all view functions in this module
# todo: show user only his/her dataset/objects : Coreobject.responsible = Dataset.owner = self.request.user


def test(request):
    from dashboard.forms import TestForm
    # todo: to delete this view, it's only for development purposes
    """
    FOR TESTING PURPOSES ONLY
    """
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = TestForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            datasets = form.cleaned_data['datasets']
            status = form.cleaned_data['status']
            print("Datasets selected: ", datasets)
            print("Status selected: ", status)

    return render(request, 'test.html', {'form': form})


@cache_page(60 * 60)
def index(request):
    """
    Base view function for the home page.
    """
    return render(request, 'index.html')


def dashboard_index(request):
    """
    Core view to render the dashboard.html template with required data
    """
    coreobjects = CoreObject.objects.all()
    paginated_obj_list, chart_data = get_dashboard_data(request, coreobjects)
    form = DashboardFilterForm()
    return render(request, 'dashboard.html', {
        'paginated_obj_list': paginated_obj_list,
        'chart_data': chart_data,
        'form': form,
    })


def get_dashboard_data(request, coreobjects):
    """
    Generates data that is required for dashboard.html template: object list, chart values, dataset names
    """
    paginated_obj_list = coreobject_paginator(request, coreobjects)
    chart_data = get_data_for_chart(coreobjects)
    return paginated_obj_list, chart_data


def coreobject_paginator(request, coreobjects):
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


def filter_form(request):
    """
    Dashboard Filter, button "Apply Filters"
    This view's purpose is to validate the obtained form, perform queries to obtain filtered data,
    and return JsonResponse with filtered data for the object table and chart.
    It also returns the form instance to fill the form with previously selected filter values.
    """
    data = dict()
    if request.method == 'POST':
        form = DashboardFilterForm(request.POST)
        if form.is_valid():

            data['form_is_valid'] = True

            dataset_filter_values = form.cleaned_data.get('datasets')
            status_filter_values = form.cleaned_data.get('status')
            priority_filter_values = form.cleaned_data.get('priority')
            timeframe_filter_values = form.cleaned_data.get('timeframe')

            coreobjects = get_filtered_coreobjects(
                dataset_filter_values, status_filter_values, priority_filter_values, timeframe_filter_values)

            paginated_obj_list, chart_data = get_dashboard_data(request, coreobjects)

            data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
                'paginated_obj_list': paginated_obj_list
            })

            data['html_chart_data'] = chart_data

        else:
            data['form_is_valid'] = False

    return JsonResponse(data)


def get_filtered_coreobjects(
        dataset_filter_values, status_filter_values, priority_filter_values, timeframe_filter_values):

    coreobjects = CoreObject.objects.all()

    if '*' in dataset_filter_values:
        dataset_filter_values = coreobjects.values_list('dataset', flat=True)

    if '*' in status_filter_values:
        status_filter_values = ['Red', 'Orange', 'Green']

    if '*' in priority_filter_values:
        priority_filter_values = ['High', 'Moderate', 'Low']

    if '*' in timeframe_filter_values:
        timeframe_filter_values = ['Day', 'Week', 'Month', 'Year']

    filtered_coreobjects = coreobjects.filter(
        dataset__in=dataset_filter_values,
        status__in=status_filter_values,
        priority__in=priority_filter_values,
        timeframe__in=timeframe_filter_values,
        )

    return filtered_coreobjects
