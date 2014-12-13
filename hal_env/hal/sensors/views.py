from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from sensors.models import Sensor, SensorData
import datetime


def index(request):
    template = loader.get_template('sensors/index.html')
    
    sensors_list = Sensor.objects.all()
    
    for sensor in sensors_list :
    	sensor.data = sensor.get_latest_point()
        temp = float(sensor.data['value'])
        sensor.data['value_f'] = temp * 1.80  + 32.00
        sensor.data['pTimestamp'] = datetime.datetime.fromtimestamp(float(sensor.data['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')

    context = {'sensors_list' : sensors_list}
    
    return render(request,'sensors/index.html', context)


def sensorView(request, sensor_id):
    template = loader.get_template('sensors/sensor.html')
    