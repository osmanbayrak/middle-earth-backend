# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    point = models.IntegerField(blank=True, null=True)

    @property
    def town(self):
        return Towns.objects.filter(whom=self)

    def __str__(self):
        return self.user.username


class Towns(models.Model):
    name = models.CharField(max_length=30, blank=True)
    military = models.IntegerField(blank=True, null=True)
    whom = models.ForeignKey(Profile, null=True, related_name="towns")





