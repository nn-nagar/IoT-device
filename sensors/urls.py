from django.conf.urls import url, include
from sensors import views
from .views import SensorViewSet, DeviceRetrieveTimeRangeViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'devices', SensorViewSet, base_name='devices')
# router.register(r'retrieve', DeviceRetrieveTimeRangeViewSet, base_name='retrieve-devices')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),

]

standard_view_urlpatterns = [
    url(r'^retrieve/$', DeviceRetrieveTimeRangeViewSet.as_view({'get': 'list'}), name='retrieve-create-get-all'),

    url(r'^retrieve/(?P<pk>[0-9a-z-]+)/$', DeviceRetrieveTimeRangeViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }), name='devices-update')
]

standard_view_urlpatterns = format_suffix_patterns(standard_view_urlpatterns)

urlpatterns += standard_view_urlpatterns



