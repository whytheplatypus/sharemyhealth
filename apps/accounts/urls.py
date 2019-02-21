

# Copyright Videntity Systems, Inc.
from django.conf.urls import url
from .views.core import account_settings, my_logout
from .views.user_profile import oidc_userprofile, oidc_userprofile_test
urlpatterns = [

    url(r'^logout', my_logout, name='my_logout'),
    url(r'^settings', account_settings, name='account_settings'),
    url(r'^userprofile-test', oidc_userprofile_test, name='user_profile_test'),
    url(r'^userprofile', oidc_userprofile, name='user_profile'),

]
