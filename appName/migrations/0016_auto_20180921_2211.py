# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-21 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0015_auto_20180921_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, choices=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East'), ('center', 'Inside')], max_length=30, null=True)),
                ('town', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='appName.Towns')),
            ],
        ),
        migrations.RemoveField(
            model_name='troop',
            name='town',
        ),
        migrations.RemoveField(
            model_name='troop',
            name='town_position',
        ),
        migrations.AddField(
            model_name='troop',
            name='town_zone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='troops', to='appName.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='zone',
            unique_together=set([('town', 'name')]),
        ),
    ]
