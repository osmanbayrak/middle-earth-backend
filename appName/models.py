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

    @property
    def score(self):
        return self.town.level * 25

    def __str__(self):
        return self.user.username


class Towns(models.Model):
    name = models.CharField(max_length=30, blank=True)
    military = models.IntegerField(blank=True, null=True)
    whom = models.ForeignKey(Profile, null=True, related_name="towns")

    def __str__(self):
        return self.name


class Building(models.Model):
    type = models.CharField(max_length=30, blank=True)
    level = models.IntegerField(blank=True, null=True, default=1)
    town = models.ForeignKey(Towns, null=True, related_name="buildings")
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, blank=True, null=True, default="loading")

    @property
    def img(self):
        return '%s%s/%s%s' % ('/images/', self.type, str(self.level), '.jpg')

    @property
    def construction_time(self):
        return self.level * 20

    def __str__(self):
        return self.type






