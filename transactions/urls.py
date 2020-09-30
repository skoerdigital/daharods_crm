from django.conf.urls import url


from .views import (
    TransactionListView,
    TransactionAllListView
)

urlpatterns = [
    url(r'^all/', TransactionAllListView.as_view(), name='list-all'),
    url(r'$', TransactionListView.as_view(), name='list')
] 