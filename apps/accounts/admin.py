from django.contrib import admin
from .models import (UserProfile)

# Copyright Videntity Systems Inc.

__author__ = "Alan Viars"


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'birth_date', 'sex', 'subject')
    search_fields = [
        'user__first_name',
        'user__last_name',
        'birth_date',
        'sex', ]
    raw_id_fields = ("user", )


admin.site.register(UserProfile, UserProfileAdmin)
