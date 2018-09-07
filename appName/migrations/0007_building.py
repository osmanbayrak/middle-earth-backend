# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-06 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0006_auto_20180906_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=30)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('town', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='appName.Towns')),
            ],
        ),
    ]
