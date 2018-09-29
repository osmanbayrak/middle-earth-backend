# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from django.db.models import Q
from django.core.validators import MaxValueValidator

TROOP_TYPES = (
        ("lancer", "Lancer"),
        ("cavalry", "Cavalry"),
        ("archer", "Archer"))
BUILDING_TYPES = (
        ("timber", "Timber"),
        ("main", "Main building"),
        ("stone", "Quarry"),
        ("barrack", "Barrack"),
        ("stable", "Stable"),
        ("farm", "Farm"),
        ("depot", "Depot"),
        ("house", "House"),
        ("archery", "Archery"))

BUILDING_STATUSES=(
    ("loading", "Under construction"),
    ("completed", "Completed")
)
TROOP_STATUSES = (
    ("preparing", "Preparing"),
    ("ready", "Ready to fight")
)
TROOP_TOWN_POSITIONS = (
    ("north", "Defend North"),
    ("south", "Defend South"),
    ("west", "Defend West"),
    ("east", "Defend East"),
    ("center", "Defend Town Center")
)


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
    name = models.CharField(max_length=15, unique=True)
    military = models.IntegerField(blank=True, null=True)
    whom = models.ForeignKey(Profile, null=True, related_name="towns")
    resources = JSONField(default={'wood': 1000, 'food': 1000, 'stone': 1000})
    building_queue = models.IntegerField(default=0)
    troop_queue = models.IntegerField(default=0)
    x_coord = models.IntegerField(null=False, validators=[MaxValueValidator(300)], default=random.randint(10, 300))
    y_coord = models.IntegerField(null=False, validators=[MaxValueValidator(300)], default=random.randint(10, 300))

    class Meta:
        unique_together = ("x_coord", "y_coord",)

    @property
    def population_limit(self):
        try:
            house = self.buildings.get(type="house").level
            main = self.buildings.get(type="main").level
            return (7 + (2**house + 2**main))*10
        except:
            return 9*10

    @property
    def building_process_limit(self):
        try:
            result = self.population_limit**(1./4.)
            if result == 0:
                return 1
            else:
                return int(result)
        except:
            return 1

    @property
    def military_process_limit(self):
        try:
            result = 1
            military_buildings = self.buildings.filter(Q(type="stable") | Q(type="barrack") | Q(type="archery"))
            for i in military_buildings:
                result += i.level
            result = result/5
            if result == 0:
                return 1
            else:
                return int(result)
        except:
            return 1

    @property
    def population(self):
        return self.troops.count()*10

    @property
    def production(self):
        timber = self.buildings.get(type="timber")
        stone = self.buildings.get(type="stone")
        farm = self.buildings.get(type="farm")
        depot = self.buildings.get(type="depot")
        return {
                "perHour": {"wood": (float((timber.level ** 3 + timber.level*60))/200 + timber.level+1)*180,
                            "food": (float((farm.level ** 3 + farm.level * 60)) / 200 + farm.level + 1)*180,
                            "stone": (float((stone.level ** 3 + stone.level * 60)) / 200 + stone.level + 2)*180
                        },
                "extraCapacity": {
                    "stone": stone.level * 150 + (stone.level * 4) ** 2,
                    "food": farm.level * 150 + (farm.level * 4) ** 2,
                    "wood": timber.level * 150 + (timber.level * 4) ** 2
                        },
                "totalCapacity": {
                    "wood": (depot.level*5)**2 + depot.level*400 + timber.level*150 + (timber.level*4)**2 + 3500,
                    "food": (depot.level * 5) ** 2 + depot.level * 400 + farm.level * 150 + (farm.level * 4) ** 2 + 3500,
                    "stone": (depot.level * 5) ** 2 + depot.level * 400 + stone.level * 150 + (stone.level * 4) ** 2 + 3500
                        }
             }

    def __str__(self):
        return self.name


class Building(models.Model):
    type = models.CharField(choices=BUILDING_TYPES, max_length=30, blank=False, null=False)
    level = models.IntegerField(default=1)
    town = models.ForeignKey(Towns, related_name="buildings")
    created_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=BUILDING_STATUSES, max_length=30, default="completed")

    class Meta:
        unique_together = ("town", "type",)

    @property
    def img(self):
        return '%s%s/%s%s' % ('images/buildings/', self.type, str(self.level), '.png')

    @property
    def construction_time(self):
        if self.type == "main":
            return int(self.level * 300 + (self.level ** 3)*5)
        else:
            mainLevel = self.town.buildings.get(type="main").level
            if self.level == 0:
                result = 180-(mainLevel**(22./6.))
                if result > 0:
                    return int(result)
                else:
                    return 10
            else:
                result = (self.level * 300 + (self.level ** 3)*5) - (mainLevel**(22./6.))
                if result > 0:
                    return int(result)
                else:
                    return 10

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
                return {"wood": self.level * 1000 + self.level ** 4, "stone": self.level * 700 + self.level ** 3}
        elif self.type == "stable":
            if self.level == 0:
                return {"wood": 1000, "stone": 2000}
            else:
                return {"wood": self.level * 1000 + self.level ** 4, "stone": self.level * 2000 + self.level ** 4}
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

    @property
    def sector(self):
        if self.type == "timber" or self.type == "stone" or self.type == "farm":
            return "production"
        elif self.type == "barrack" or self.type == "stable" or self.type == "archery":
            return "military"
        else:
            return "others"

    def __str__(self):
        return self.type


class Troop(models.Model):
    type = models.CharField(choices=TROOP_TYPES, max_length=30)
    tier = models.IntegerField(default=0)
    town = models.ForeignKey(Towns, related_name="troops")
    created_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=TROOP_STATUSES, max_length=30, default="preparing")
    town_position = models.CharField(choices=TROOP_TOWN_POSITIONS, max_length=30, default="center")

    @property
    def cost(self):
        if self.type == "lancer":
            if self.tier == 0:
                return {"wood": 250, "stone": 300, "food": 800}
            else:
                return {"wood": self.tier * 150 + self.tier ** 3, "stone": self.tier * 250 + self.tier ** 4, "food": self.tier * 500 + self.tier ** 5}
        elif self.type == "archer":
            if self.tier == 0:
                return {"wood": 400, "stone": 300, "food": 900}
            else:
                return {"wood": self.tier * 300 + self.tier ** 4, "stone": self.tier * 200 + self.tier ** 3, "food": self.tier * 550 + self.tier ** 5}
        elif self.type == "cavalry":
            if self.tier == 0:
                return {"wood": 650, "stone": 500, "food": 2500}
            else:
                return {"wood": self.tier * 500 + self.tier ** 4, "stone": self.tier * 350 + self.tier ** 5, "food": self.tier * 800 + self.tier ** 6}

    @property
    def power(self):
        if self.type == "lancer":
            return self.tier**3 + self.tier*100
        elif self.type == "archer":
            return self.tier**4 + self.tier*200
        elif self.type == "cavalry":
            return self.tier**5 + self.tier*400

    @property
    def img(self):
        return '%s%s/%s%s' % ('images/military/', self.type, str(self.tier), '.png')

    @property
    def preparation_time(self):
        if self.type == "lancer":
            buildingLevel = self.town.buildings.get(type="barrack", town=self.town.id).level
            if self.tier == 0:
                result = 360 - (buildingLevel ** (22. / 6.))
                if result > 0:
                    return int(result)
                else:
                    return 15
            else:
                return int(self.tier * 420 + self.tier ** 3 - (buildingLevel ** (22. / 6.)))
        elif self.type == "archer":
            buildingLevel = self.town.buildings.get(type="archery").level
            if self.tier == 0:
                result = 480 - (buildingLevel ** (22. / 6.))
                if result > 0:
                    return int(result)
                else:
                    return 15
            else:
                return int(self.tier * 480 + self.tier ** 3 - (buildingLevel ** (22. / 6.)))
        elif self.type == "cavalry":
            buildingLevel = self.town.buildings.get(type="stable").level
            if self.tier == 0:
                result = 840 - (buildingLevel ** (22. / 6.))
                if result > 0:
                    return int(result)
                else:
                    return 15
            else:
                return int(self.tier * 620 + self.tier ** 3 - (buildingLevel ** (22. / 6.)))






