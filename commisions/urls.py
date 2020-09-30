from django.conf.urls import url


from .views import (
    confirm,
    accept,
    deny
)

urlpatterns = [
    url(r'^(?P<pk>[\w-]+)/$', confirm, name='confirm'),
    url(r'^(?P<pk>[\w-]+)/accept/$', accept, name='accept'),
    url(r'^(?P<pk>[\w-]+)/deny/$', deny, name='deny'),
]