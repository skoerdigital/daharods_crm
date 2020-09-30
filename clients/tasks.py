from celery.task.schedules import crontab
from celery.decorators import periodic_task

from celery.decorators import task
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
import operator
from functools import reduce

from django.db.models import Q

from .models import Client
from notifications.models import Notification 

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='0', hour='0')), name="birthday_notification_task", ignore_result=True)
def birthday_notification_task():
    now = datetime.now()
    then = now + timedelta(3)

    monthdays = [(now.month, now.day)]
    while now <= then:
        monthdays.append((now.month, now.day))
        now += timedelta(days=1)
    monthdays = (dict(zip(("birthday__month", "birthday__day"), t)) for t in monthdays)
    query = reduce(operator.or_, (Q(**d) for d in monthdays))
    client_birthdays = Client.objects.filter(query)

    if client_birthdays:
        for client in client_birthdays:
            notification = Notification.objects.create(category='B', content='Twój klient ' + client.name + ' ' +client.surname + ' obchodzi urodziny za 3 dni.', content_object=client)
            notification.receivers.add(client.owner)
            notification.save()