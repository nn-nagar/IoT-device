from rest_framework.serializers import ModelSerializer
from .models import Device


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_uuid', 'sensor_type', 'sensor_value', 'sensor_reading_time']

    def validate(self, attrs):
        instance = Device(**attrs)
        instance.clean()
        return attrs


class DeviceTimeSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_uuid', 'sensor_type', 'sensor_value', 'sensor_reading_time']
