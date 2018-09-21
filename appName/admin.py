# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import Towns
from models import Building
from models import Profile
from models import Troop
from django.contrib.auth.models import User

from django.contrib import admin

admin.register(Towns)
admin.register(Building)
admin.register(Profile)
admin.register(User)
admin.register(Troop)
