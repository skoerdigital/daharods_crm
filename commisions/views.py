#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create your views here.
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Commision

@login_required()
def confirm(request, pk):
    if request.method=='POST' and request.is_ajax():
        try:
            obj = Commision.objects.get(pk=pk)
            obj.data_attr = request.POST['transaction']
            obj.request = True
            obj.state = 'P'
            obj.save()
            return JsonResponse({'done': True, 'status':'Powodzenie', 'msg': 'Prośba została pomyślnie wysłana'})
        except Commision.DoesNotExist:
            return JsonResponse({'done': False, 'status':'Błąd', 'msg': 'Transakcja nie istnieje'})
    else:
        return JsonResponse({'done': False, 'status':'Błąd', 'msg':'Wystąpił nieznany błąd. Skontaktuj się z administratorem lub spróbuj ponownie później'})


@login_required()
def accept(request, pk):
    if request.method=='POST' and request.is_ajax():
        try:
            obj = Commision.objects.get(pk=pk)
            obj.state = 'A'
            obj.accepted = True
            obj.save()
            return JsonResponse({'done': True, 'status':'Powodzenie', 'msg': 'Wypłata prowizji została zaakceptowana'})
        except Commision.DoesNotExist:
            return JsonResponse({'done': False, 'status':'Błąd', 'msg': 'Transakcja nie istnieje'})
    else:
        return JsonResponse({'done': False, 'status':'Błąd', 'msg':'Wystąpił nieznany błąd. Skontaktuj się z administratorem lub spróbuj ponownie później'})


@login_required()
def deny(request, pk):
    if request.method=='POST' and request.is_ajax():
        try:
            obj = Commision.objects.get(pk=pk)
            obj.state = 'D'
            obj.accepted = False
            obj.save()
            return JsonResponse({'done': True, 'status':'Powodzenie', 'msg': 'Wypłata prowizji została odrzucona'})
        except Commision.DoesNotExist:
            return JsonResponse({'done': False, 'status':'Błąd', 'msg': 'Transakcja nie istnieje'})
    else:
        return JsonResponse({'done': False, 'status':'Błąd', 'msg':'Wystąpił nieznany błąd. Skontaktuj się z administratorem lub spróbuj ponownie później'})
