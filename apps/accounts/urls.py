

# Copyright Videntity Systems, Inc.
from django.conf.urls import url
from .views.core import (account_settings,
                         mylogout)
urlpatterns = [
    url(r'^logout', mylogout, name='mylogout'),
    url(r'^settings', account_settings, name='account_settings'),



]
