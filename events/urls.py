from django.conf.urls import url

from .views import (
    EventListView,
    EventListAllView,
    AjaxEventCreateView,
    AjaxEventUpdateView,
    AjaxEventDeleteView
)

urlpatterns = [
    url(r'^create/$', AjaxEventCreateView.as_view(), name='create'),
    url(r'^all/$', EventListAllView.as_view(), name='list-all'),
    url(r'^(?P<id>[\w-]+)/edit/$', AjaxEventUpdateView.as_view(), name='edit'),
    url(r'^(?P<id>[\w-]+)/delete/$', AjaxEventDeleteView.as_view(), name='delete'),
    url(r'$', EventListView.as_view(), name='list') 
]