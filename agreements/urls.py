from django.conf.urls import url


from .views import (
    AgreementCreateView,
    AgreementDetailView,
    AgreementListView,
    AgreementListAllView,
    AgreementUpdateView
)

urlpatterns = [
    url(r'^create/$', AgreementCreateView.as_view(), name='create'),
    url(r'^all/$', AgreementListAllView.as_view(), name='list-all'),
    url(r'^(?P<nr>[\w-]+)/$', AgreementDetailView.as_view(), name='detail'),
    url(r'^(?P<nr>[\w-]+)/edit/$', AgreementUpdateView.as_view(), name='edit'),
    url(r'$', AgreementListView.as_view(), name='list')
] 