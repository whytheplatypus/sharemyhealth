from django.conf.urls import url
from django.contrib import admin
from .views import cda_in_json, cda_as_xml

admin.autodiscover()

urlpatterns = [

    url(r'cda-in-json', cda_in_json, name='cda_in_json'),
    url(r'cda', cda_as_xml, name='cda_as_xml'),
]
