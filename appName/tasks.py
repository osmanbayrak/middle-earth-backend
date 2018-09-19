from celery import Celery
from celery.schedules import crontab
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins
from Serializer import *
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, status
from models import *
from datetime import timedelta, time
import datetime
import pytz

utc = pytz.UTC

app = Celery('tasks', broker='amqp://guest@localhost:5672//')


@app.task()
def add(x, y):
    builts = Building.objects.filter(status="loading")
    towns = Towns.objects.all()
    for i in builts:
        if (i.change_date + (timedelta(seconds=i.construction_time))).replace(tzinfo=utc) <= (datetime.datetime.now()).replace(tzinfo=utc):
            builts.filter(id=i.id).update(status="completed", level=i.level+1)



@app.task
def myuniq():
    towns = Towns.objects.all()
    for i in towns:
        towns.filter(id=i.id).update(resources={"wood": float(i.resources["wood"]) + float((i.buildings.get(type="timber").level ** 3 + i.buildings.get(type="timber").level*120))/360,
                                                "stone": float(i.resources["stone"]) + float((i.buildings.get(type="stone").level ** 3 + i.buildings.get(type="stone").level*120))/360,
                                                "food": float(i.resources["food"]) + float((i.buildings.get(type="farm").level ** 3 + i.buildings.get(type="farm").level*120))/360})
