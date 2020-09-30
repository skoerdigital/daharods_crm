# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import prevent_recursion

import decimal
import datetime

# from employees.models import Employee
# from agreements.models import Declaration, Agreement

User = settings.AUTH_USER_MODEL
transaction = {
    'product_id': None,
    'client_id': None,
    'owner': None,
    'amount': None,
    'fee': None,
    'valid_since': None,
    'valid_to': None
}

class Transaction(models.Model):
    product_id = models.ForeignKey('products.Product')
    client_id = models.ForeignKey('clients.Client')
    owner = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=17, decimal_places=2)
    fee = models.DecimalField(max_digits=17, decimal_places=2)
    valid_since = models.DateField(auto_now=False, auto_now_add=False)
    valid_to = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def time_left(self):
        now = datetime.date.today()
        duration = self.valid_to - self.valid_since
        time_left = now - self.valid_since
        if duration.days != 0:
            return round((time_left.days/duration.days)*100,0)
        else:
            return 'Time to short'

    def __str__(self):
        return str(self.amount) + ' ' + str(self.id)

@receiver(post_save, sender='agreements.Declaration')
def create_transaction(sender, instance, created, **kwargs):    
    if created:
        transaction['product_id'] = instance.product_id
        transaction['fee'] = instance.product_id.parameter.value
        transaction['client_id'] = instance.client_id
    if not created:
        transaction['product_id'] = instance.product_id
        transaction['fee'] = instance.product_id.parameter.value
        transaction['client_id'] = instance.client_id


@receiver(post_save, sender='agreements.Agreement')
def save_transaction(sender, instance, created, **kwargs):
    if created:
        transaction['owner'] = instance.owner
        transaction['amount'] = instance.amount
        transaction['valid_since'] = instance.valid_since
        transaction['valid_to'] = instance.valid_to
        if None not in transaction.values():
            Transaction.objects.update_or_create(product_id=transaction['product_id'], client_id=transaction['client_id'], owner=transaction['owner'], amount=transaction['amount'], fee=transaction['fee']*transaction['amount'], valid_since=transaction['valid_since'], valid_to=transaction['valid_to'])
    if not created:
        transaction['owner'] = instance.owner
        transaction['amount'] = instance.amount
        transaction['valid_since'] = instance.valid_since
        transaction['valid_to'] = instance.valid_to
        if None not in transaction.values():
            Transaction.objects.filter(id=instance.id).update( product_id=transaction['product_id'], client_id=transaction['client_id'], owner=transaction['owner'], amount=transaction['amount'], fee=transaction['fee']*transaction['amount'], valid_since=transaction['valid_since'], valid_to=transaction['valid_to'])