from celery import Celery
from django.db.models import F

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
            Towns.objects.filter(id=i.town.id).update(building_queue=F('building_queue')-1)


@app.task()
def military_check():
    preparing_troops = Troop.objects.filter(status="preparing")
    for i in preparing_troops:
        if i.change_date:
            if (i.change_date.replace(tzinfo=utc) + (timedelta(seconds=i.preparation_time))).replace(tzinfo=utc) <= (datetime.datetime.now()).replace(tzinfo=utc):
                preparing_troops.filter(id=i.id).update(status="ready", tier=i.tier + 1)
                Towns.objects.filter(id=i.town.id).update(troop_queue=F('troop_queue') - 1)
        else:
            print '%s%s' % (i.id, "id li troop change date secmedi!")
            preparing_troops.filter(id=i.id).update(status="ready")


@app.task
def town_check():
    towns = Towns.objects.all()
    for i in towns:
        loading_que = []
        preparing_que = []
        try:
            towns.filter(id=i.id).update(resources={"wood": float(i.resources["wood"]) + float((i.buildings.get(type="timber").level ** 3 + i.buildings.get(type="timber").level*120))/100 + 1,
                                                "stone": float(i.resources["stone"]) + float((i.buildings.get(type="stone").level ** 3 + i.buildings.get(type="stone").level*120))/100 + 2,
                                                "food": float(i.resources["food"]) + float((i.buildings.get(type="farm").level ** 3 + i.buildings.get(type="farm").level*120))/100 + 1})

            buildings = Building.objects.filter(status="loading", town=i.id)
            for j in buildings:
                loading_que.append(j)
            towns.filter(id=i.id).update(building_queue=len(loading_que))

            troops = Troop.objects.filter(status="preparing", town=i.id)
            for j in troops:
                preparing_que.append(j)
            towns.filter(id=i.id).update(troop_queue=len(preparing_que))

        except:
            return None
