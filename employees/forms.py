#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import Employee
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('user','employee_nr')
        labels = {
            "name": "Imię",
            "surname": "Nazwisko",
            "employee_state": "Status",
            "role": "Uprawnienia"
        }

class UserMailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            "name": "E-mail",
        }


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
