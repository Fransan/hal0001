from django.conf.urls import patterns, include, url
from sensors import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<sensor_id>\d+)/$', views.sensorView, name='sensorView')
)