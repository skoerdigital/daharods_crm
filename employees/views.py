# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseNotFound, HttpResponseForbidden
from crm.mixins.ajaxformresponse import AjaxFormResponseMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from multi_form_view import MultiModelFormView

from .models import Employee
from agreements.models import Agreement
from contacts.models import Contact
from clients.models import Client
from .forms import EmployeeForm, UserMailForm, UserCreateForm

User = get_user_model()

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'employees/employee_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        if self.request.user.employee.role == 'E':
            if username != self.request.user.username:
                raise PermissionDenied
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(*args, **kwargs)
        context['us'] = self.object
        context['employees'] = Employee.objects.all()
        return context
    
class EmployeeListView(LoginRequiredMixin, ListView):
    template_name = 'employees/employee_list.html'

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.request.user.employee.role is 'A':
            return self.render_to_response(context)
        else:
            raise PermissionDenied

class EmployeeCreateView(LoginRequiredMixin, MultiModelFormView, CreateView):
    form_classes = {
        'user_form' : UserCreateForm,
        'employee_form' : EmployeeForm
    }

    template_name = 'employees/employee_create_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if self.request.user.employee.role is 'A':
            return self.render_to_response(context)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('employees:list')
    
    def get_context_data(self, *args, **kwargs):
        context = super(EmployeeCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Dodaj pracownika'
        return context

    def forms_valid(self, forms):
        user = forms['user_form'].save(commit=False)
        employee = forms['employee_form'].save(commit=False)
        user.is_staff = user.is_active = user.is_superuser = True
        user.save()
        employee.user = user
        employee.save()
        return super(EmployeeCreateView, self).forms_valid(forms)

class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'employees/employee_form.html'
    form_class = EmployeeForm
    model = Employee

    def get_object(self, *args, **kwargs):
        user = User.objects.get(username=self.kwargs.get("username"))
        if user is None:
            raise Http404
        if self.request.user.employee.role == 'E':
            if user != self.request.user:
                raise PermissionDenied
        return Employee.objects.get(user=user)


    def get_context_data(self, *args, **kwargs):
        data = super(EmployeeUpdateView, self).get_context_data(*args, **kwargs)
        data['title'] = "Edytuj dane użytkownika"
        if self.request.POST:
            data['email'] = UserMailForm(self.request.POST, instance=self.object.user)
        else:
            data['email'] = UserMailForm(instance=self.object.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        email_form = context['email'].save(commit=False)
        self.get_object().user.email = email_form.email
        email_form.save()
        return super(EmployeeUpdateView, self).form_valid(form)

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'employees/employee_password_change.html'
    success_url = reverse_lazy('employees:detail')

    def get_success_url(self, *args, **kwargs):
        print(kwargs)
        return reverse_lazy('employees:detail', kwargs = {'username': self.kwargs['username']})


@login_required()
def data_migrate(request):
    
    if request.method=='POST' and request.is_ajax():
        migrate_user = User.objects.get(username=request.POST['toMigrate'])
        current_user = User.objects.get(username=request.POST['current'])
        agreements_list = Agreement.objects.filter(owner=migrate_user)
        contacts_list = Contact.objects.filter(owner=migrate_user)
        client_list = Client.objects.filter(owner=migrate_user)

        for agreement in agreements_list:
            agreement.owner = current_user
            agreement.save()

        for contact in contacts_list:
            contact.owner = current_user
            contact.save()

        for client in client_list:
            client.owner = current_user
            client.save()

        return JsonResponse({'done': True, 'status':'Powodzenie', 'msg': 'Baza została pomyślnie przypisana'})
    else:
        return JsonResponse({'done': False, 'status':'Błąd', 'msg':'Wystąpił nieznany błąd. Skontaktuj się z administratorem lub spróbuj ponownie później'})

   