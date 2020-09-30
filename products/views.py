# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from crm.mixins.ajaxformresponse import AjaxFormResponseMixin
from crm.shortcuts.shortcuts import get_object_or_json404
from .models import ProductType, Product, ProductParameter
from .forms import ProductCreateForm, ProductParameterCreateForm


from .models import Product, ProductType


class ProductsListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = Product.objects.all()
        return qs
    
    def get_context_data(self, *args, **kwargs):
        data = super(ProductsListView, self).get_context_data(*args, **kwargs)
        data['product_types'] = ProductType.objects.values_list('name', flat=True).distinct()
        return data

class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'products/product_form.html'
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:list')

    def get_context_data(self, *args, **kwargs):
        if self.request.user.employee.role is 'A':
            data = super(ProductCreateView, self).get_context_data(*args, **kwargs)
            data['title'] = 'Dodaj produkt'
            if self.request.POST:
                data['parameter'] = ProductParameterCreateForm(self.request.POST)
            else:
                data['parameter'] = ProductParameterCreateForm()
            return data
        else:
            raise PermissionDenied

    def form_valid(self, form):
        context = self.get_context_data()
        parameter_form = context['parameter']
        with transaction.atomic():
            product = form.save(commit=False)
            product.owner = self.request.user
            if form.has_changed():
                product.save()
            if parameter_form.is_valid() and form.is_valid():
                parameter = parameter_form.save(commit=False)
                parameter.product = product
                parameter.save()
        return super(ProductCreateView, self).form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'products/product_form.html'
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:list')

    def get_object(self, *args, **kwargs):
        if self.request.user.employee.role == 'E':
            raise PermissionDenied
        return Product.objects.get(code=self.kwargs.get("code"))

    def get_context_data(self, *args, **kwargs):
        data = super(ProductUpdateView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Dodaj produkt'
        
        if self.request.POST:
            data['parameter'] = ProductParameterCreateForm(self.request.POST,instance=self.object.parameter)
        else:
            data['parameter'] = ProductParameterCreateForm(instance=self.object.parameter)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        parameter_form = context['parameter']
        with transaction.atomic():
            product = form.save(commit=False)
            product.owner = self.request.user
            if form.has_changed():
                product.save()
            if parameter_form.is_valid() and form.is_valid():
                parameter = parameter_form.save(commit=False)
                parameter.product = product
                parameter.save()
        return super(ProductUpdateView, self).form_valid(form)



class AjaxProductTypeCreateView(LoginRequiredMixin, AjaxFormResponseMixin, CreateView):
    model = ProductType
    fields = ('name', 'description')

    def get_object(self, queryset=None):
        return get_object_or_json404(ProductType, pk=self.kwargs['pk'])

    def get_context_data(self, context):
        context['success'] = True
        return context