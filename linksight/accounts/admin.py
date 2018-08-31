import csv

from django.contrib import admin
from django.http import HttpResponse
from linksight.accounts.models import Survey


class ExportCsvMixin:
    """
    Taken from:
    https://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    """
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = 'Export selected'


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_filter = ('profession', 'organization', 'has_gis_experience')
    actions = ['export_as_csv']
