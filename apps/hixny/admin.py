from django.contrib import admin
from .models import HIXNYProfile

# Copyright Videntity Systems Inc.

__author__ = "Alan Viars"


class HIXNYProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'mrn',)
    search_fields = [
        'user__first_name',
        'user__last_name',
        'mrn', ]
    raw_id_fields = ("user", )


admin.site.register(HIXNYProfile, HIXNYProfileAdmin)
