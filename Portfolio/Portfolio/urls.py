# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^shop/', include('shop.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^order/', include('orders.urls')),
]

handler404 = 'shop.views.error_404'
handler500 = 'shop.views.error_500'