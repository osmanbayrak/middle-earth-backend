# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-23 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0021_auto_20180923_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='towns',
            name='building_process_limit',
            field=models.IntegerField(blank=True, default=2),
        ),
        migrations.AddField(
            model_name='towns',
            name='military_process_limit',
            field=models.IntegerField(blank=True, default=2),
        ),
    ]
