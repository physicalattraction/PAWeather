from django.contrib import admin

from measurements.models import HourlyMeasurement
from stations.models import Station


@admin.register(HourlyMeasurement)
class HourlyMeasurementAdmin(admin.ModelAdmin):
    # fields = ['station', 'day', 'hour', 'precipitation', 'sunshine']
    exclude = None

    list_display = ['station_id', 'day', 'hour', 'precipitation', 'sunshine']
    list_filter = ['station']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('day', 'hour')
        return queryset