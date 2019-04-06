from django.conf.urls import url
from django.contrib import admin
from .views import get_authorization, approve_authorization

admin.autodiscover()

urlpatterns = [
    url(r'get-authorization$', get_authorization, name='hixny_get_authorization'),
    url(r'approve-authorization$', approve_authorization, name='approve_get_authorization'),
    # url(r'display-authorization$', display_fhir_endpoint_with_id, name='fhir_endpoint_with_id_oauth'),
    # url(r'baseDstu3/(?P<fhir_resource>[^/]+)/$', fhir_endpoint_search, name='fhir_endpoint_search_oauth'),
]
