# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-23 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0019_auto_20180922_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='towns',
            name='building_queue',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='towns',
            name='troop_queue',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
