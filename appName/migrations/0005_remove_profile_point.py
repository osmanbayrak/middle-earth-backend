# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-10 22:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0004_auto_20180910_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='point',
        ),
    ]
