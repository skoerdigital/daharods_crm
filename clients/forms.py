#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import Client, ClientAddress, ClientContactData
from django_countries.fields import LazyTypedChoiceField
from django_countries.widgets import CountrySelectWidget
from crm.settings.base import DATE_INPUT_FORMATS

class ClientCreateForm(forms.ModelForm):
    GENDERS = [('K','Kobieta'), ('M','Mężczyzna')]
    STATES = [('A','Aktywny'), ('U','Zarchiwizowany')]
    DOC_TYPE = [('D','Dowód osobisty'), ('P','Paszport'), ('I','Inny')]
    gender = forms.ChoiceField(choices=GENDERS,widget=forms.RadioSelect())
    client_state = forms.ChoiceField(choices=STATES,widget=forms.RadioSelect())
    doc_type = forms.ChoiceField(choices=DOC_TYPE,widget=forms.RadioSelect())
    birthday = forms.DateField(input_formats=DATE_INPUT_FORMATS)
    class Meta:
        model = Client
        exclude = ('owner','slug', 'client_id')


ClientFormSet = inlineformset_factory(Client, ClientAddress, extra=0, min_num=1, max_num=3, exclude=('gender','slug', 'client_id'))
ContactFormSet = inlineformset_factory(Client, ClientContactData, extra=0, min_num=1, max_num=10, exclude=('client_id',))
