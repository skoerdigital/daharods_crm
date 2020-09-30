from django.conf.urls import url


from .views import (
    ContactsListView,
    ContactsDetailView,
    AjaxContactCreateView,
    AjaxContactUpdateView
)

urlpatterns = [
    url(r'^create/$', AjaxContactCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[\w-]+)/update/$', AjaxContactUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[\w-]+)/$', ContactsDetailView.as_view(), name='detail'),
    url(r'$', ContactsListView.as_view(), name='list')
]