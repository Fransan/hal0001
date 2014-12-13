from django.db import models

# Create your models here.
class Sensor(models.Model):
    SENSOR_TYPES =(
        ('temperature', 'temperature'),
    )
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 50,
                            choices = SENSOR_TYPES)
    description = models.TextField()
    
    def get_latest_point(self):
        for data in SensorData.objects.filter(sensor_id__exact = self.id).order_by('-timestamp')[:1]:
            point = dict(value = str(data.value), timestamp = str(data.timestamp)) 
            
        return point
    
    
    def __unicode__(self):
        return '%s' % (self.name)
    
class SensorData (models.Model):
    sensor_id = models.ForeignKey(Sensor)
    value = models.IntegerField()
    timestamp = models.BigIntegerField()
    
    def __unicode__(self):
        return '%s' % (self.value)