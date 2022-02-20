from django.test import tag, TestCase, SimpleTestCase
from django.utils.timezone import now
from django.urls import resolve
from sensors.models import Device
from django.urls.base import reverse

from rest_framework.test import APIClient
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO
from unittest.mock import patch, Mock


def setup_view_callable(view, request, *args, **kwargs):
    """
     Mimic as_view() callable at urls resolvers
     Returns view instance
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class FTTest_HomePage(SimpleTestCase):

    def test_url_resolve_correct(self):
        found = resolve('/')
        self.assertEqual(found.view_name, 'home-page')

    def test_url_returns_correct_Template(self):
        response = self.client.get(
            reverse('home-page')
        )
        self.assertTemplateUsed(response, 'sensors/home.html')
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf8')
        self.assertIn('<title>sensors app</title>', html)


class Sensor_API_Test(TestCase):
    def setUp(self):
        super().setUp()
        device0 = Device(sensor_value=50.0)
        device0.save()
        device1 = Device(sensor_value=89.0, sensor_reading_time=now())
        device1.save()
        self.first = device0

    def test_Can_Retrieve_one_record(self):
        device = Device.objects.all()[0]
        client = APIClient()
        uuids = str(device)[:]
        response = client.get(f'/sensors/devices/{uuids}/')
        self.assertEqual(response.status_code, 200)
        stream = BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 4)








