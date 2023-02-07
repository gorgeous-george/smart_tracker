from django.contrib import admin

from core_app.models import Dataset, CoreObject


class CoreObjectAdmin(admin.ModelAdmin):
    list_filter = ('dataset', 'status', 'responsible')
    list_display = ('dataset', 'name', 'status', 'responsible')
    sortable_by = ('dataset', 'status', 'responsible')


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'description')


admin.site.register(CoreObject, CoreObjectAdmin)
admin.site.register(Dataset, DatasetAdmin)
