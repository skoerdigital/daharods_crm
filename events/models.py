from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from crm.shortcuts.request import get_username
from crm.test import testmethod

User = settings.AUTH_USER_MODEL

class Event(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    start = models.DateTimeField(auto_now=False, auto_now_add=False)
    end = models.DateTimeField(auto_now=False, auto_now_add=False)
    is_allday = models.BooleanField(default=False)
    contact = models.ForeignKey('contacts.Contact', blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.owner =  get_username().user
        super(Event, self).save(*args, **kwargs)
