from django.conf.urls import url
from django.contrib import admin
from .views import (fhir_endpoint_with_id, fhir_endpoint_search)

admin.autodiscover()

urlpatterns = [
    url(r'baseDstu3/(?P<fhir_resource>[^/]+)/(?P<id>[^/]+)/$', fhir_endpoint_with_id, name='fhir_endpoint_with_id_oauth'),
    url(r'baseDstu3/(?P<fhir_resource>[^/]+)/$', fhir_endpoint_search, name='fhir_endpoint_search_oauth'),
]
