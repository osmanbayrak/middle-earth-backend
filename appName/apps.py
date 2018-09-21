# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AppNameConfig(AppConfig):
    name = 'appName'

    def ready(self):
        super(AppNameConfig, self).ready()
        from appName.tasks import military_check
        from appName.tasks import building_check
        from appName.tasks import town_check