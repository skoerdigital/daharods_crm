from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from django.db.models import Count, Sum
from crm.mixins.ajaxformresponse import AjaxFormResponseMixin
from django.http import JsonResponse
from crm.shortcuts.shortcuts import get_object_or_json404
from django.contrib.auth import get_user_model
from .models import Event
from employees.models import Employee
from clients.models import Client
from contacts.models import Contact

User = get_user_model()


    
class EventListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(EventListView, self).get_context_data(*args, **kwargs)
        context['contacts'] = Contact.objects.filter(owner=self.request.user)
        return context


class EventListAllView(LoginRequiredMixin, ListView):
    template_name = 'events/events_all_list.html'

    def get_queryset(self):
        return Event.objects.all()

    def get_context_data(self,*args,**kwargs):
        
        if 'usr' in self.request.GET and self.request.GET['usr'] is not "":
            usr = Employee.objects.get(id=self.request.GET['usr']).user
        else:
            usr = self.request.user
        context = super(EventListAllView, self).get_context_data(*args, **kwargs)
        context['events_count'] =  User.objects.annotate(event_count=Count('event')).values('event_count', 'employee__name', 'employee__surname')
        context['meetings_count'] = Contact.objects.filter(is_appointed=True, owner=usr).annotate(year=ExtractYear('timestamp'), month=ExtractMonth('timestamp')).values('month', 'year').annotate(count=Count('timestamp')).values('month', 'year', 'count')
        
        return context

     
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        if self.request.user.employee.role is 'A':
            return self.render_to_response(context)
        else:
            raise PermissionDenied


class AjaxEventCreateView(LoginRequiredMixin, AjaxFormResponseMixin, CreateView):
    model = Event
    fields = ('title', 'color', 'is_allday', 'start', 'end','description',)

    def get_context_data(self, context, **kwargs):
        context['event_id'] = self.object.id
        context['success'] = True
        return context
    
    # def post(self, request, *args, **kwargs):
    #     print("sss dziala")
    #     self.object = None
    #     return super(AjaxEventCreateView, self).post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     self.object = form.save()
    #     return super(AjaxEventCreateView, self).form_valid(form)


class AjaxEventUpdateView(LoginRequiredMixin, AjaxFormResponseMixin, UpdateView):
    model = Event
    fields = ('title', 'color', 'is_allday', 'start', 'end','description',)

    def get_object(self, queryset=None):
        return get_object_or_json404(Event, id=self.kwargs['id'])

    def get_context_data(self, context, **kwargs):
        context['event_id'] = self.object.id
        context['success'] = True
        return context

class AjaxEventDeleteView(LoginRequiredMixin, AjaxFormResponseMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:list')

    def get_object(self, queryset=None):
        return get_object_or_json404(Event, id=self.kwargs['id'])

    def get_context_data(self, context, **kwargs):
        context['success'] = True
        return context