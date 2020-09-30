from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from crm.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

class ProductType(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    ACTIVE = 'A'
    UNACTIVE = 'U'
    CHOICES = (
        (ACTIVE, 'Aktywny'),
        (UNACTIVE, 'Nieaktywny')
    )
    owner = models.ForeignKey(User)
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    state = models.CharField(max_length=1, choices=CHOICES, default=ACTIVE)
    product_type = models.ForeignKey(ProductType, related_name="product_type")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'code': self.code})

class ProductParameter(models.Model):
    product = models.OneToOneField(Product, related_name="parameter")
    value = models.DecimalField(max_digits=20, decimal_places=4)
    client_fee = models.DecimalField(max_digits=20, decimal_places=4)
    duration = models.DecimalField(max_digits=2, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
