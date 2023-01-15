from django.contrib import admin

from core_app.models import CoreObject


class CoreObjectAdmin(admin.ModelAdmin):
    list_filter = ('obj_type', 'status', 'responsible')
    list_display = ('obj_type', 'name', 'status', 'responsible')
    sortable_by = ('obj_type', 'status', 'responsible')


admin.site.register(CoreObject, CoreObjectAdmin)
