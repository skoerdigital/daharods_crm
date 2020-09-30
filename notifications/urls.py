from django.conf.urls import url

from .views import (
    is_shown,
    send,
    NotificationListView
)

urlpatterns = [
    url(r'^read/$', is_shown, name='read'),
    url(r'^send/$', send, name='send'),
    url(r'^$', NotificationListView.as_view(), name='list'),     
]