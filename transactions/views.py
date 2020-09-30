#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

# Create your views here.
from .models import Transaction
from products.models import Product


class TransactionAllListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.request.user.employee.role == 'A':
            return self.render_to_response(context)
        else:
            raise PermissionDenied

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionAllListView, self).get_context_data(*args, **kwargs)

        products_usage = []

        product_ids = Transaction.objects.all().values_list('product_id', flat=True)
        products_used = Product.objects.filter(id__in=product_ids.distinct())
        transactions_count = Transaction.objects.values('product_id').annotate(total=Count('product_id')).order_by()
        
        context['usage'] = products_usage
        context['product_categories'] = products_used
        return context

class TransactionListView(LoginRequiredMixin, ListView):

    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(owner=self.request.user)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionListView, self).get_context_data(*args, **kwargs)

        products_usage = []

        product_ids = Transaction.objects.all().values_list('product_id', flat=True)
        products_used = Product.objects.filter(id__in=product_ids.distinct())
        transactions_count = Transaction.objects.values('product_id').annotate(total=Count('product_id')).order_by()
        
        context['usage'] = products_usage
        context['product_categories'] = products_used
        return context
