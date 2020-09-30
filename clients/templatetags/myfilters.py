#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
import calendar
import locale
from agreements.models import Agreement

#locale.setlocale(locale.LC_ALL, 'pl_PL')

register = template.Library()

@register.filter(name='add_attributes')
def add_attributes(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)


@register.filter
def state(value):
    if value is 'A':
        value = 'AKTYWNY'
    elif value is 'U':
        value = 'NIEAKTYWNY'
    return value

@register.filter
def doc_type(value):
    if value is 'D':
        value = 'Dowód osobisty'
    elif value is 'P':
        value = 'Paszport'
    else:
        value = 'Inny'
    return value

@register.filter
def address_type(value):
    if value is 'R':
        value = 'Adres zameldowania'
    elif value is 'C':
        value = 'Adres kontaktowy'
    elif value is 'A':
        value = 'Adres zamieszkania'
    else:
        value = 'Inny'
    return value

@register.filter
def contact_type(value):
    if value is 'E':
        value = 'E-mail'
    elif value is 'T':
        value = 'Telefon'
    else:
        value = 'Inny'
    return value

@register.filter
def role(value):
    if value is 'E':
        value = 'PRACOWNIK'
    elif value is 'A':
        value = 'ADMINISTRATOR'
    else:
        value = 'Inny'
    return value


@register.filter
def is_none(value):
    if value is None:
        value = 0
    return value

@register.filter
def dot_comma(value):
    return str(value).replace(',','.')


@register.filter
def as_percentage(value):
    value = str(value*100)[:-2] +'%'
    return value


@register.filter
def strip_double_quotes(quoted_string):
    return quoted_string.replace('"', '')


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]


@register.filter
def get_agreement_nr(commision_nr):
    agreement = Agreement.objects.get(id=commision_nr)
    return agreement.nr


@register.filter
def to_int(value):
    value = int(value)
    return value
