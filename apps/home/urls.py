from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from .views import authenticated_home

admin.autodiscover()

urlpatterns = [
    url(r'', authenticated_home, name='home'),

]
