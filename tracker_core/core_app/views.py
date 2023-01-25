from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from core_app.models import CoreObject
from core_app.forms import CoreObjectModelForm

def index(request):
    """
    View function for the home page
    """
    return render(request, 'index.html')

def coreobject_list(request):
    coreobjects = CoreObject.objects.all()
    return render(request, 'coreobject_list.html', {'coreobjects': coreobjects})


def save_coreobject_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            coreobjects = CoreObject.objects.all()
            data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
                'coreobjects': coreobjects
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def coreobject_create(request):
    if request.method == 'POST':
        form = CoreObjectModelForm(request.POST)
    else:
        form = CoreObjectModelForm()
    return save_coreobject_form(request, form, 'includes/partial_coreobject_create.html')


def coreobject_update(request, pk):
    coreobject = get_object_or_404(CoreObject, pk=pk)
    if request.method == 'POST':
        form = CoreObjectModelForm(request.POST, instance=coreobject)
    else:
        form = CoreObjectModelForm(instance=coreobject)
    return save_coreobject_form(request, form, 'includes/partial_coreobject_update.html')


def coreobject_delete(request, pk):
    coreobject = get_object_or_404(CoreObject, pk=pk)
    data = dict()
    if request.method == 'POST':
        coreobject.delete()
        data['form_is_valid'] = True
        coreobjects = CoreObject.objects.all()
        data['html_coreobject_list'] = render_to_string('includes/partial_coreobject_list.html', {
            'coreobjects': coreobjects
        })
    else:
        context = {'coreobject': coreobject}
        data['html_form'] = render_to_string('includes/partial_coreobject_delete.html', context, request=request)
    return JsonResponse(data)
