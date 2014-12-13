# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.BinaryField()),
                ('timestamp', models.BigIntegerField()),
                ('sensor_id', models.ForeignKey(to='sensors.Sensor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
