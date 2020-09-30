from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response, HttpResponseRedirect
from django.db import transaction
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Max
from django.core.exceptions import PermissionDenied

from .models import Client, ClientAddress, ClientContactData
from .forms import ClientCreateForm, ClientFormSet, ContactFormSet
from transactions.models import Transaction
from agreements.models import Agreement


class ClientsListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        return Client.objects.filter(owner=self.request.user)


class ClientsListAllView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = Client.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.request.user.employee.role is 'A':
            return self.render_to_response(context)
        else:
            raise PermissionDenied


class ClientDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self, *args, **kwargs):
        if self.request.user.employee.role == 'A':
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        client = Client.objects.get(slug__iexact=self.kwargs['slug'])
        context['total_amount'] = Transaction.objects.filter(client_id=client).aggregate(Sum('amount'))['amount__sum']
        context['total_fee'] = Transaction.objects.filter(client_id=client).aggregate(Sum('fee'))['fee__sum']
        context['max_amount'] = Transaction.objects.filter(client_id=client).aggregate(Max('amount'))['amount__max']
        return context
        

class ClientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'clients/client_form.html'
    model = Client
    form_class = ClientCreateForm

    def get_context_data(self, *args, **kwargs):
        data = super(ClientCreateView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Dodaj klienta'
        if self.request.POST:
            data['clientaddress'] = ClientFormSet(self.request.POST)
            data['clientcontact'] = ContactFormSet(self.request.POST)
        else:
            data['clientaddress'] = ClientFormSet()
            data['clientcontact'] = ContactFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        clientaddress = context['clientaddress']
        clientcontact = context['clientcontact']
        with transaction.atomic():
            client = form.save(commit=False)
            client.owner = self.request.user
            if form.has_changed():
                client.save()
            if clientaddress.is_valid() and form.is_valid() and clientcontact.is_valid():
                self.object = form.save()
                clientaddress.instance = self.object
                clientaddress.save()
                self.object = clientcontact.save(commit=False)
                for contact in self.object:
                    contact.client_id = client
                    contact.save()
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientCreateForm
    template_name = 'clients/client_form.html'

    def get_context_data(self, *args, **kwargs):
        data = super(ClientUpdateView, self).get_context_data(*args, **kwargs)
        data['title'] = 'Edytuj dane klienta'
        if self.request.POST:
            data['clientaddress'] = ClientFormSet(self.request.POST, instance=self.object)
            data['clientcontact'] = ContactFormSet(self.request.POST, instance=self.object)
        else:
            data['clientaddress'] = ClientFormSet(instance=self.object)
            data['clientcontact'] = ContactFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        clientaddress = context['clientaddress']
        clientcontact = context['clientcontact']
        with transaction.atomic():
            client = form.save(commit=False)
            client.owner = self.request.user
            if form.has_changed():
                client.save()
            if clientaddress.is_valid() and form.is_valid() and clientcontact.is_valid():
                self.object = form.save()
                clientaddress.instance = self.object
                clientaddress.save()
                self.object = clientcontact.save(commit=False)
                for contact in self.object:
                    contact.client_id = client
                    contact.save()
                clientcontact.save()
        return super(ClientUpdateView, self).form_valid(form)