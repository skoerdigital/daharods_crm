from django.conf.urls import url


from .views import (
    ProductsListView,
    ProductCreateView,
    AjaxProductTypeCreateView,
    ProductUpdateView
)

urlpatterns = [
    url(r'^create/type/$', AjaxProductTypeCreateView.as_view(), name='create-type'),
    url(r'^create/$', ProductCreateView.as_view(), name='create'),
    url(r'^(?P<code>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='edit'),
    url(r'$', ProductsListView.as_view(), name='list')
]