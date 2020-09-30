from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from crm.shortcuts.shortcuts import get_object_or_json404

from crm.mixins.ajaxformresponse import AjaxFormResponseMixin

from .models import Contact

class ContactsListView(LoginRequiredMixin, ListView):
    def get_queryset(self, *args, **kwargs):
        return Contact.objects.all()


class ContactsDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self, *args, **kwargs):
        return Contact.objects.all()
        


class AjaxContactCreateView(LoginRequiredMixin, AjaxFormResponseMixin, CreateView):
    model = Contact
    fields = ('name', 'surname', 'email', 'tel')

    def get_object(self, queryset=None):
        return get_object_or_json404(Contact, pk=self.kwargs['pk'])

    def get_context_data(self, context):
        context['success'] = True
        return context
    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.owner = self.request.user
        contact.save()
        return super(AjaxContactCreateView, self).form_valid(form)

class AjaxContactUpdateView(LoginRequiredMixin, AjaxFormResponseMixin, UpdateView):
    model = Contact
    fields = ('is_appointed',)

    def get_object(self, queryset=None):
        return get_object_or_json404(Contact, pk=self.kwargs['pk'])

    def get_context_data(self, context):
        context['success'] = True
        return context

    # def form_valid(self, form):
    #     contact = form.save(commit=False)
    #     contact.is_appointed = True
    #     contact.owner = self.request.user
    #     contact.save()
    #     return super(AjaxContactUpdateView, self).form_valid(form)

