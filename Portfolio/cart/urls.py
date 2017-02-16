# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'cart'
urlpatterns = [
    url(r'^add_product_front/$', views.add_product_front, name='add_product_front'),
    url(r'^$', views.CartDetail, name='CartDetail'),
    url(r'^remove/(?P<product_id>\d+)/$', views.CartRemove, name='CartRemove'),
    url(r'^add/(?P<product_id>\d+)/$', views.CartAdd, name='CartAdd'),
    url(r'^add_one_or_remove/$', views.add_one_or_remove, name='add_one_or_remove'),
    url(r'^remove_all/$', views.remove_all, name='remove_all'),
    ]