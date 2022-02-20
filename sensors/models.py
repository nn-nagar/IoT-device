from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
import uuid


# Create your models here.
class Device(models.Model):
    """
      Device data model
    """
    device_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)
    SENSOR_TYPE = (('pressure', 'Pressure'),
                  ('temperature', 'Temperature'))
    sensor_type = models.CharField(max_length=80, choices=SENSOR_TYPE,
                                   blank=False, null=False,
                                   default='temperature')
    sensor_value = models.DecimalField(max_digits=5, decimal_places=1, null=False, blank=False)
    sensor_reading_time = models.DateTimeField(default=now)

    def __str__(self):
        return '{}'.format(self.device_uuid)

    def save(self, *args, **kwargs):
        try:
            self.clean()
            super(Device, self).save()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]

    def clean(self, **kwargs):
        if self.sensor_value > 100.0:
            raise ValidationError('Sensor value cannot be grater than 100.0')
        else:
            pass









