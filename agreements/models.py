# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Agreement(models.Model):
    
    ACTIVE = 'A'
    UNACTIVE = 'U'
    TAG_CHOICES = (
        (ACTIVE, 'Aktywny'),
        (UNACTIVE, 'Nieaktywny')
    )
    
    client_id = models.ForeignKey('clients.Client')
    owner = models.ForeignKey(User)
    buyer = models.ForeignKey(User, related_name="buyer")
    valid_since = models.DateField(auto_now=False, auto_now_add=False)
    valid_to = models.DateField(auto_now=False, auto_now_add=False)
    nr = models.CharField(max_length=20)
    state = models.CharField(max_length=1, choices=TAG_CHOICES, default=ACTIVE)
    amount = models.DecimalField(max_digits=17, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('agreements:detail', kwargs={'nr': self.nr})

    def __str__(self):
        return str(self.id) + ' ' + str(self.client_id)

class Declaration(models.Model):
    client_id = models.ForeignKey('clients.Client')
    product_id = models.ForeignKey('products.Product')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.client_id)