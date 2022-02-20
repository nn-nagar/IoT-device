from django.test import TestCase
from sensors.models import Device
from django.utils.timezone import now


class DeviceModelTest(TestCase):

    def test_Device_Model_has_attributes(self):
        sensor = Device()
        self.assertEqual(sensor.sensor_type, 'temperature')

    def test_Can_Device_Retrieve_Data(self):
        device0 = Device.objects.create(sensor_value=2.0, sensor_type='humility')
        device1 = Device.objects.create(sensor_value=1.1, sensor_type='humility')
        self.assertEqual(
            list(Device.objects.all()),
            [device0, device1]
        )

