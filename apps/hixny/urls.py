from django.conf.urls import url
from django.contrib import admin
from .views import get_authorization, approve_authorization
from .api_views import get_cda_in_json, get_cda_raw, get_cda_in_json_test, get_cda_raw_test

admin.autodiscover()

urlpatterns = [
    url(r'get-authorization$', get_authorization, name='hixny_get_authorization'),
    url(r'approve-authorization$', approve_authorization,
        name='approve_get_authorization'),
    url(r'api/cda-in-json$', get_cda_in_json, name='get_ cda_in_json'),
    url(r'api/cda$', get_cda_raw, name='get_cda_raw'),
    url(r'api/cda-in-json-test$', get_cda_in_json_test,
        name='get_cda_in_json_test'),
    url(r'api/cda-test$', get_cda_raw_test, name='get_cda_raw_test'),

]
