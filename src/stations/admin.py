from django.contrib import admin

from stations.models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'latitude', 'longitude', 'altitude']
    list_display = fields
