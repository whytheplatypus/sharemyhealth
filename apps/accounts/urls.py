

# Copyright Videntity Systems, Inc.
from django.conf.urls import url
from .views.core import (account_settings, )
urlpatterns = [
    url(r'^settings', account_settings, name='account_settings'),
]
