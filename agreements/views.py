# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404, reverse
from django.http import Http404
from django.db import transaction
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dateutil.relativedelta import relativedelta
from django.core.exceptions import PermissionDenied

from multi_form_view import MultiModelFormView

from .models import Agreement, Declaration
from .forms import AgreementCreateForm, DeclarationCreateForm

class AgreementListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = Agreement.objects.filter(owner=self.request.user)
        return qs

class AgreementListAllView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        qs = Agreement.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.request.user.employee.role is 'A':
            return self.render_to_response(context)
        else:
            raise PermissionDenied

class AgreementDetailView(LoginRequiredMixin, DetailView):

    def get_object(self):
        nr = self.kwargs.get('nr')
        if nr is None:
            raise Http404
        if self.request.user.employee.role == 'E':
            return get_object_or_404(Agreement, nr__iexact=nr, owner=self.request.user)
        return get_object_or_404(Agreement, nr__iexact=nr)

    def get_context_data(self, *args, **kwargs):
        context = super(AgreementDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Umowa nr'
        id = self.get_object().id
        if id is None:
            raise Http404
        context['declaration'] = Declaration.objects.get(id=id)
        return context

class AgreementCreateView(LoginRequiredMixin, MultiModelFormView, CreateView):
    form_classes = {
        'agreement_form' : AgreementCreateForm,
        'declaration_form' : DeclarationCreateForm,
    }
    nr = None
    template_name = 'agreements/agreement_form.html'

    def get_success_url(self):
        return reverse('agreements:detail', kwargs={'nr': self.nr})
    
    def get_context_data(self, *args, **kwargs):
        context = super(AgreementCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Dodaj umowę'
        return context

    def forms_valid(self, forms):
        with transaction.atomic():
            agreement = forms['agreement_form'].save(commit=False)
            self.nr = agreement.nr 
            agreement.owner = self.request.user 
            declaration = forms['declaration_form'].save(commit=False)
            agreement.valid_to = agreement.valid_since + relativedelta(years=declaration.product_id.parameter.duration)
            declaration.client_id = agreement.client_id
            declaration.save()
            agreement.save()
        return super(AgreementCreateView, self).forms_valid(forms)


class AgreementUpdateView(LoginRequiredMixin, MultiModelFormView, UpdateView):
    form_classes = {
        'agreement_form' : AgreementCreateForm,
        'declaration_form' : DeclarationCreateForm,
    }
    nr = None
    template_name = 'agreements/agreement_form.html'

    def get_objects(self):
        self.nr = self.kwargs.get('nr', None)
        try:
            agreement = Agreement.objects.get(nr=self.nr)
            print(agreement.id)
        except Agreement.DoesNotExist:
            agreement = None
        return {
            'agreement_form': agreement,
            'declaration_form': Declaration.objects.get(id=agreement.id)
        }

    def get_context_data(self, *args, **kwargs):
        context = super(AgreementUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Edytuj umowę'
        return context

    def get_success_url(self):
        return reverse('agreements:detail', kwargs={'nr': self.nr})

    def forms_valid(self, forms):
        with transaction.atomic():
            agreement = forms['agreement_form'].save()
            self.nr = agreement.nr 
            agreement.save()
            declaration = forms['declaration_form'].save(commit=False)
            agreement.valid_to = agreement.valid_since + relativedelta(years=declaration.product_id.parameter.duration)
            declaration.client_id = agreement.client_id
            declaration.save()
            agreement.save()
        
        return super(AgreementUpdateView, self).forms_valid(forms)
