from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, DetailView, UpdateView
from core_app.models import CoreObject


def index(request):
    """
    View function for the home page
    """
    return render(request, 'index.html')


# todo: to delete after testing (also url and template)
def test_view(request):
    return render(request, 'test.html')


class CoreObjectListView(LoginRequiredMixin, ListView):
    """
    Generic class-based list view for all core objects available.
    """
    model = CoreObject
    paginate_by = 10
    template_name = "coreobject_list.html"

    def get_queryset(self):
        """
        Return list of all CoreObject objects
        """
        queryset = CoreObject.objects.all()
        return queryset


class CoreObjectDetailView(LoginRequiredMixin, DetailView):
    """
    Generic class-based detailed view for a particular object.
    """
    model = CoreObject
    template_name = "coreobject_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['object_list'] = CoreObject.objects.all()
        return context


class CoreObjectCreateView(LoginRequiredMixin, CreateView):
    model = CoreObject
    template_name = "coreobject_form.html"
    fields = [
        "name",
        "description",
        "obj_type",
        "measure",
        "_measure_limit",
        "measure_unit",
        "status",
        "lifelong_period",
        "responsible",
    ]


class CoreObjectUpdateView(LoginRequiredMixin, UpdateView):
    model = CoreObject
    template_name = "coreobject_form.html"
    fields = [
        "name",
        "description",
        "obj_type",
        "measure",
        "_measure_limit",
        "measure_unit",
        "status",
        "lifelong_period",
        "responsible",
    ]


class CoreObjectDeleteView(LoginRequiredMixin, DeleteView):
    model = CoreObject
    template_name = "coreobject_confirm_delete.html"
    success_url = reverse_lazy('coreobject-list')
