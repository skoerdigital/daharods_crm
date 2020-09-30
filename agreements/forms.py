#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import inlineformset_factory
from .models import Agreement, Declaration

class AgreementCreateForm(forms.ModelForm):
    valid_since = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    class Meta:
        model = Agreement
        exclude = ('owner', 'valid_to')
    def clean_nr(self):
        nr = self.cleaned_data.get('nr', False)
        if nr.find('/')!=-1 or nr.find("\'")!=-1:
            raise forms.ValidationError('Numer umowy nie jest prawidłowy')
        return self.cleaned_data["nr"] 
        
class DeclarationCreateForm(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = ['product_id']
