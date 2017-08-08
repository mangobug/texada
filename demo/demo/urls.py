# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from .views import ExportView, ExportAllView, HomePageView, ProductCreate, \
                    ProductView, ProductUpdate
from .views import delete_product, upload_file


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^product/(?P<pk>\d+)/$', ProductView.as_view(), name='product_view'),
    url(r'^create/product/$', ProductCreate.as_view(), name='product_create'),
    url(r'^update/product/(?P<pk>\d+)/$', ProductUpdate.as_view(), name='product_update'),
    url(r'^delete/product/$', delete_product, name='delete_product'),

    url(r'^export/$', ExportAllView.as_view(), name='export_all_data'),
    url(r'^export/data/$', ExportView.as_view(), name='export_data'),
    url(r'^export/data/(?P<product_id>\d+)/$', ExportView.as_view(), name='export_data'),
    url(r'^import/data/$', upload_file, name='upload_file'),

    url(r'^admin/', admin.site.urls),
]
