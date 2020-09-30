#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Notification(models.Model):
    BIRTHDAY = 'B'
    EVENT = 'E'
    COMMISION_REQUEST = 'R'
    COMMISION_DECISION = 'D'
    MESSAGE = 'M'
    CATEGORY_CHOICES = (
        (BIRTHDAY, 'Birthday'),
        (EVENT, 'Event'),
        (COMMISION_REQUEST, 'Commision - request'),
        (COMMISION_DECISION, 'Commision - decision'),
        (MESSAGE, 'Message'),
    )
    receivers = models.ManyToManyField(User)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default=None)
    content = models.CharField(max_length=150)
    is_shown = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = fields.GenericForeignKey('content_type', 'object_id')


@receiver(post_save, sender='commisions.Commision')
def notification_transaction(sender, instance, created, **kwargs):    
    if not created:
        if instance.state == 'P':
            users_admin = list(User.objects.prefetch_related('employee').filter(employee__role='A'))  
            notification = Notification.objects.create(category='R', content='Nowa prośba o wypłatę prowizji od ' + instance.owner.employee.name + ' ' + instance.owner.employee.surname, content_object=instance)
            notification.receivers.add(*users_admin)
            notification.save()
        if instance.state == 'A' or instance.state == 'D':
            content = None
            if instance.state == 'A':
                content = 'Twoja prośba o wypłatę prowizji została zaakceptowana'
            elif instance.state == 'D':
                content = 'Twoja prośba o wypłatę prowizji została odrzucona'
            notification = Notification.objects.create(category='D', content=content, content_object=instance)
            notification.receivers.add(instance.owner)
            notification.save()

            
