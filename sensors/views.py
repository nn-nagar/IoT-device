from django.shortcuts import render
from .models import Device
from .serializers import DeviceSerializer, DeviceTimeSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.generic import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from django_filters import rest_framework as filters
import django_filters
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class TemplateBase(TemplateView):
    """
     view that returns base template
    """
    def get(self, request, *args, **kwargs):

        template_name = 'base.html'
        return render(request, template_name)


class TemplateHome(TemplateView):
    """
    view that returns home template
    """
    def get(self, request, *args, **kwargs):
        template_name = 'sensors/home.html'
        return render(request, template_name)


class SimpleHelloWorld(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>hello world</h1>')


class SensorViewSet(ModelViewSet):

    """
     POST and PUT : create and update
    """
    permission_classes = (IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = (filters.DjangoFilterBackend,)


class DeviceTimeFilter(django_filters.FilterSet):

    sensor_type = django_filters.CharFilter(field_name='sensor_type', lookup_expr='exact')
    start_time = django_filters.DateTimeFilter(field_name='sensor_reading_time', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name='sensor_reading_time', lookup_expr='lte')

    class Meta:
        model = Device
        fields = ['sensor_type', 'start_time', 'end_time']


class DeviceRetrieveTimeRangeViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceTimeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = DeviceTimeFilter




