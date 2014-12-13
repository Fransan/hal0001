from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from sensors.models import Sensor, SensorData
import datetime, time


def index(request):
    template = loader.get_template('sensors/index.html')
    
    sensors_list = Sensor.objects.all()
    
    for sensor in sensors_list :
    	sensor.data = sensor.get_latest_point()
        temp = float(sensor.data['value'])
        sensor.data['value_f'] = temp * 1.80  + 32.00
        sensor.data['pTimestamp'] = datetime.datetime.fromtimestamp(float(sensor.data['timestamp'])).strftime('%Y-%m-%d %H:%M')

    context = {'sensors_list' : sensors_list}
    
    return render(request,'sensors/index.html', context)


def sensorView(request, sensor_id):
    template = loader.get_template('sensors/sensor.html')
    now = int(time.time())
    start = now - 86400
    sensor = Sensor.objects.get(id=sensor_id)
    sensor_data = SensorData.objects.filter(timestamp__range=(start,now),sensor_id=sensor_id)
    
    sen = sensor.__dict__
    sen['data'] = {'value': [], 'timestamp': []} 
        
    for data in sensor_data:
        sen['data']['value'].append(float(str(data.value)))
        sen['data']['timestamp'].append(str(data.timestamp * 1000))
        
    
    sen['data']['value'] = str(sen['data']['value'])[1:-1]
    sen['data']['timestamp'] = str(sen['data']['timestamp'])[1:-1]
    sen['max'] = 'NA' 
    sen['min'] = 'NA'
    sen['avg'] = 'NA'
    
    context = {'sensor' : sen}
    
    return render(request,'sensors/sensor.html', context)