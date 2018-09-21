from celery import Celery
from models import *
from datetime import timedelta, time
import datetime
import pytz

utc = pytz.UTC

app = Celery('tasks', broker='amqp://guest@localhost:5672//')


@app.task()
def building_check():
    builts = Building.objects.filter(status="loading")
    for i in builts:
        if (i.change_date + (timedelta(seconds=i.construction_time))).replace(tzinfo=utc) <= (datetime.datetime.now()).replace(tzinfo=utc):
            builts.filter(id=i.id).update(status="completed", level=i.level+1)


@app.task()
def military_check():
    preparing_troops = Troop.objects.filter(status="preparing")
    for i in preparing_troops:
        if i.change_date:
            if (i.change_date + (timedelta(seconds=i.preparation_time))).replace(tzinfo=utc) <= (datetime.datetime.now()).replace(tzinfo=utc):
                preparing_troops.filter(id=i.id).update(status="ready", tier=i.tier + 1)
        else:
            print i.id + "id li troop change date secmedi!"
# def add(x, y):
#     builts = Building.objects.filter(status="completed")
#     for i in builts:
#         builts.filter(id=i.id).update(status="completed", level=0)


@app.task
def town_check():
    towns = Towns.objects.all()
    for i in towns:
        try:
            towns.filter(id=i.id).update(resources={"wood": float(i.resources["wood"]) + float((i.buildings.get(type="timber").level ** 3 + i.buildings.get(type="timber").level*120))/100,
                                                "stone": float(i.resources["stone"]) + float((i.buildings.get(type="stone").level ** 3 + i.buildings.get(type="stone").level*120))/100,
                                                "food": float(i.resources["food"]) + float((i.buildings.get(type="farm").level ** 3 + i.buildings.get(type="farm").level*120))/100})
        except Exception:
            print i.name + "town has no resources building!"
