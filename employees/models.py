from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string


User = settings.AUTH_USER_MODEL

class Employee(models.Model):
    EMPLOYEE = 'E'
    ADMIN = 'A'
    ROLES = (
        (EMPLOYEE, 'Pracownik'),
        (ADMIN, 'Administrator')
    )

    ACTIVE = 'A'
    UNACTIVE = 'U'
    STATE = (
        (ACTIVE, 'Aktywny'),
        (UNACTIVE, 'Nieaktywny')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    employee_nr = models.CharField(max_length=20, blank=True)
    employee_state = models.CharField(max_length=1, choices=STATE, default=ACTIVE)
    role = models.CharField(max_length=1, choices=ROLES, default=EMPLOYEE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' ' + self.surname

    def get_absolute_url(self):
        return reverse('employees:detail', kwargs={'username': self.user.username})

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.employee_nr = self.name[0:3].lower()+self.surname[0:3].lower()+'-'+get_random_string(length=6)
        super(Employee, self).save(*args, **kwargs)
