# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from employees.models import Employee

class Role(models.Model):
    name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Permission(models.Model):
    employee = models.ForeignKey('employees.Employee')
    role = models.ForeignKey(Role)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)