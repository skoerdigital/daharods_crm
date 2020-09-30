from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django_countries.fields import CountryField
from datetime import datetime
from django.contrib.contenttypes.fields import GenericRelation

from crm.utils import unique_slug_generator, client_id_generator

User = settings.AUTH_USER_MODEL


class Client(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now().strftime("%Y-%m-%d"))
    gender = models.CharField(max_length=1)
    city = models.CharField(max_length=100)
    pesel = models.DecimalField(max_digits=11, decimal_places=0)
    client_id = models.CharField(max_length=20, blank = True, null = True)
    client_state = models.CharField(max_length=1)
    doc_type = models.CharField(max_length=1)
    doc_nr = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank = True, null = True)
    notification = GenericRelation('notifications.Notification', related_query_name="clients")

    def __str__(self):
        return self.name + ' ' + self.surname + ' (' + self.client_id + ')' 

    def get_absolute_url(self):
        return reverse('clients:detail', kwargs={'slug': self.slug})


class ClientContactData(models.Model):
    EMAIL = 'E'
    TELEPHONE = 'T'
    TAG_CHOICES = (
        (EMAIL, 'E-mail'),
        (TELEPHONE, 'Numer telefonu')
    )
    client_id = models.ForeignKey(Client)
    contact_type = models.CharField(max_length=1, choices=TAG_CHOICES, default=EMAIL)
    value = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class ClientAddress(models.Model):
    REGISTERED = 'R'
    RESIDENCE = 'A'
    CONTACT = 'C'
    TAG_CHOICES = (
        (REGISTERED, 'Adres zameldowania'),
        (RESIDENCE, 'Adres zamieszkania'),
        (CONTACT, 'Adres kontaktowy')
    )
    client_id = models.ForeignKey(Client)
    contact_type = models.CharField(max_length=1, choices=TAG_CHOICES, default=REGISTERED)
    street = models.CharField(max_length=40)
    house_nr = models.CharField(max_length=20)
    apartment_nr = models.CharField(max_length=20)
    post = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=6)
    country = CountryField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.street

def client_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    if not instance.client_id:
        client_id = client_id_generator(instance)
        if Client.objects.filter(client_id=client_id).exists():
            print(Client.objects.filter(client_id=client_id).exists())
            instance.client_id = client_id_generator(instance)
        else:
            instance.client_id = client_id

pre_save.connect(client_pre_save_receiver, sender=Client)