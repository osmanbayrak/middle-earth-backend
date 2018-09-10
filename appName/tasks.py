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
    for i in builts:
        if ((i.created_date + (timedelta(seconds=i.construction_time))).replace(tzinfo=utc) <= (datetime.datetime.now()).replace(tzinfo=utc)):
            builts.filter(id=i.id).update(status="completed", level=i.level+1)


@app.task
def myuniq(x, z):
    b = x + z
    print b

