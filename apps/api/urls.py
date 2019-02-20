from django.conf.urls import url
from django.contrib import admin
from .views import CDAExample


admin.autodiscover()

urlpatterns = [
    url(r'cda', CDAExample.as_view(), name='cda'),
]
