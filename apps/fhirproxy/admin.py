from django.contrib import admin
from .models import Crosswalk

# Copyright Videntity Systems Inc.

__author__ = "Alan Viars"


class CrosswalkAdmin(admin.ModelAdmin):

    list_display = ('user', 'user_identifier', 'fhir_patient_id')
    search_fields = [
        'user__first_name',
        'user__last_name', ]
    raw_id_fields = ("user", )


admin.site.register(Crosswalk, CrosswalkAdmin)
