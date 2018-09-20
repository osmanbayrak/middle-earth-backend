# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    @property
    def town(self):
        return Towns.objects.filter(whom=self)

    @property
    def score(self):
        total = 0
        for i in self.town:
            total = i.military * 25
        return total

    def __str__(self):
        return self.user.username


class Towns(models.Model):
    name = models.CharField(max_length=30, blank=True)
    military = models.IntegerField(blank=True, null=True)
    whom = models.ForeignKey(Profile, null=True, related_name="towns")
    resources = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Building(models.Model):
    type = models.CharField(max_length=30, blank=True)
    level = models.IntegerField(blank=True, null=True, default=1)
    town = models.ForeignKey(Towns, null=True, related_name="buildings")
    created_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=30, blank=True, null=True, default="loading")

    @property
    def img(self):
        return '%s%s/%s%s' % ('images/', self.type, str(self.level), '.png')

    @property
    def construction_time(self):
        if self.level == 0:
            return 180
        else:
            return self.level * 20 + self.level ** 2

    @property
    def cost(self):
        if self.type == "main":
            if self.level == 0:
                return {"wood": 100, "stone": 150}
            else:
                return {"wood": self.level * 500 + self.level ** 6, "stone": self.level * 900 + self.level ** 7}
        elif self.type == "barrack":
            if self.level == 0:
                return {"wood": 700, "stone": 1500}
            else:
                return {"wood": self.level * 700 + self.level ** 3, "stone": self.level * 1000 + self.level ** 4}
        elif self.type == "stable":
            if self.level == 0:
                return {"wood": 1000, "stone": 2000}
            else:
                return {"wood": self.level * 1000 + self.level ** 3, "stone": self.level * 2000 + self.level ** 4}
        elif self.type == "house":
            if self.level == 0:
                return {"wood": 200, "stone": 250, "food": 1000}
            else:
                return {"wood": self.level * 350 + self.level ** 3, "stone": self.level * 500 + self.level ** 3,
                        "food": self.level * 800 + self.level **4}
        else:
            if self.level == 0:
                return {"wood": 250, "stone": 300}
            else:
                return {"wood": self.level * 350 + self.level ** 4, "stone": self.level * 500 + self.level ** 5}

    def __str__(self):
        return self.type






