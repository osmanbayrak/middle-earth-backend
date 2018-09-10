# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AppNameConfig(AppConfig):
    name = 'appName'

    def ready(self):
        super(AppNameConfig, self).ready()
        from appName.tasks import add
        from appName.tasks import myuniq