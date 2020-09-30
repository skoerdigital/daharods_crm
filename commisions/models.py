#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from transactions.models import Transaction

from django.db.models.signals import post_save
from django.dispatch import receiver

# from transactions.models import Transaction

User = settings.AUTH_USER_MODEL

class Commision(models.Model):
    INITIALIZED = 'I'
    PENDING = 'P'
    ACCEPTED = 'A'
    DENIDED = 'D'
    STATE_CHOICES = (
        (INITIALIZED, 'Zainicjalizowana'),
        (PENDING, 'Oczekiwanie na akceptację'),
        (ACCEPTED, 'Zaakceptowano'),
        (DENIDED, 'Denided')
    )
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    owner = models.ForeignKey(User)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=INITIALIZED)
    request = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender='transactions.Transaction')
def create_transaction(sender, instance, created, **kwargs):    
    if created:
        Commision.objects.update_or_create(id=instance.id, transaction=instance,owner=instance.owner, state='I', request=False, accepted=False)
        
