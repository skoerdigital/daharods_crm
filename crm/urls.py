from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    LoginView, 
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.core.urlresolvers import reverse_lazy

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(template_name='user/login.html', redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
     url(r'^password_reset/done/$',
        PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    url(r'^clients/', include('clients.urls', namespace='clients')), 
    url(r'^products/', include('products.urls', namespace='products')), 
    url(r'^agreements/', include('agreements.urls', namespace='agreements')), 
    url(r'^transactions/', include('transactions.urls', namespace='transactions')),
    url(r'^commisions/', include('commisions.urls', namespace='commisions')),
    url(r'^employees/', include('employees.urls', namespace='employees')),  
    url(r'^events/', include('events.urls', namespace='events')),  
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),  
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),  
    url(r'^$', login_required(TemplateView.as_view(template_name='index.html')), name='about'),
]
