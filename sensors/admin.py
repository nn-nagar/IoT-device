from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
# Register your models here.
from django.contrib.admin import register

from sensors.models import Device


@register(Device)
class DeviceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["device_uuid", "sensor_type", "sensor_value", "sensor_reading_time"]

