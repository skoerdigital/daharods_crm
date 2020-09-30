from django.conf.urls import url

from .views import (
    EmployeeDetailView, 
    EmployeeUpdateView, 
    UserPasswordChangeView, 
    EmployeeListView,
    EmployeeCreateView,
    data_migrate
)

urlpatterns = [
    url(r'^create/$', EmployeeCreateView.as_view(), name='create'),
    url(r'^migrate/$', data_migrate, name='migrate'),
    url(r'^(?P<username>[\w-]+)/$', EmployeeDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w-]+)/edit/$', EmployeeUpdateView.as_view(), name='edit'),
    url(r'^(?P<username>[\w-]+)/password/$', UserPasswordChangeView.as_view(), name='password'),
    url(r'$', EmployeeListView.as_view(), name='list'),
]