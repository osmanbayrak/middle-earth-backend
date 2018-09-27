# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-27 16:43
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appName', '0025_auto_20180927_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='town',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='appName.Towns'),
        ),
        migrations.AlterField(
            model_name='towns',
            name='x_coord',
            field=models.IntegerField(default=261, validators=[django.core.validators.MaxValueValidator(300)]),
        ),
        migrations.AlterField(
            model_name='towns',
            name='y_coord',
            field=models.IntegerField(default=286, validators=[django.core.validators.MaxValueValidator(300)]),
        ),
        migrations.AlterField(
            model_name='troop',
            name='town',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='troops', to='appName.Towns'),
        ),
    ]
