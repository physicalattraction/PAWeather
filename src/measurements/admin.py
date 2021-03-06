from django.contrib import admin

from measurements.models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    exclude = None

    list_display = ['station_id', 'time', 'temperature', 'precipitation', 'sunshine']
    list_filter = ['station']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('station_id', 'time')
        return queryset
