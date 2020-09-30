#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create your views here.
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Notification
from employees.models import Employee
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

@login_required()
def is_shown(request):
    if request.method=='POST' and request.is_ajax():
        notifications = Notification.objects.filter(receivers=request.user)
        for notification in notifications:
            notification.is_shown = True
            notification.save()
        return JsonResponse({'done': True, 'status':'Powodzenie', 'msg': 'Prośba została pomyślnie wysłana'})
    else:
        return JsonResponse({'done': False, 'status':'Błąd', 'msg':'Wystąpił nieznany błąd. Skontaktuj się z administratorem lub spróbuj ponownie później'})


@login_required()
def send(request):
    if request.method=='POST' and request.is_ajax():
        try:
            message = request.POST['message']
            notification = Notification.objects.create(category='M', content=message, content_type=ContentType.objects.get_for_model(User), object_id=request.user.id)
            notification.receivers.add(*list(User.objects.all()))
            notification.save()
            return JsonResponse({'done': True, 'status':'Powodzenie', 'msg': 'Prośba została pomyślnie wysłana'})
        except Notification.DoesNotExist:
            return JsonResponse({'done': False, 'status':'Błąd', 'msg': 'Transakcja nie istnieje'})
    else:
        return JsonResponse({'done': False, 'status':'Błąd', 'msg':'Wystąpił nieznany błąd. Skontaktuj się z administratorem lub spróbuj ponownie później'})


class NotificationListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = Notification.objects.filter(receivers=self.request.user)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        data = super(NotificationListView, self).get_context_data(*args, **kwargs)
        data['notifications'] = self.get_queryset()
        data['employees'] = Employee.objects.all()
        return data
