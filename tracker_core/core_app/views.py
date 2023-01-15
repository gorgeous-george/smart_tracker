from django.views.generic import ListView, DetailView
from core_app.models import CoreObject


class CoreObjectDetailView(DetailView):
    """
    Generic class-based detailed view for a particular object.
    """
    model = CoreObject


class CoreObjectListView(ListView):
    """
    Generic class-based list view for all core objects available.
    """
    model = CoreObject
    paginate_by = 5

    def get_queryset(self):
        """
        Return list of all CoreObject objects
        """
        queryset = CoreObject.objects.all()
        return queryset
