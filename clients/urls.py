from django.conf.urls import url


from .views import (
    ClientsListView,
    ClientsListAllView,
    ClientCreateView,
    ClientDetailView,
    ClientUpdateView
)

urlpatterns = [
    url(r'^create/$', ClientCreateView.as_view(), name='create'),
    url(r'^all/$', ClientsListAllView.as_view(), name='list-all'),
    url(r'^(?P<slug>[\w-]+)/$', ClientDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', ClientUpdateView.as_view(), name='edit'),
    url(r'$', ClientsListView.as_view(), name='list')
]