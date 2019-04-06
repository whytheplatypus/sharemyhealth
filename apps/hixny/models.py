from django.db import models
from django.contrib.auth import get_user_model
# Copyright Videntity Systems Inc.
__author__ = "Alan Viars"


class HIXNYProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                db_index=True, null=False)
    mrn = models.CharField(max_length=64, default='', blank=True)
    stageuser_password = models.CharField(
        max_length=64, default='', blank=True)
    stageuser_token = models.CharField(max_length=64, default='', blank=True)
    data_requestor = models.CharField(
        max_length=64, default='ActualCBOUser', blank=True)
    terms_accepted = models.TextField(default='', blank=True)
    terms_string = models.TextField(default='', blank=True)
    step_1 = models.BooleanField(default=False, blank=True)
    step_2 = models.BooleanField(default=False, blank=True)
    step_3 = models.BooleanField(default=False, blank=True)
    step_4 = models.BooleanField(default=False, blank=True)
    step_5 = models.BooleanField(default=False, blank=True)
    user_accept = models.BooleanField(default=True, blank=True)
    cda_content = models.TextField(default='', blank=True)
    cda_file = models.FileField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        display = '%s %s (%s)' % (self.user.first_name,
                                  self.user.last_name,
                                  self.user.username)
        return display

    @property
    def consent_to_share_data(self):
        if self.user_accept is True:
            return '1'
        return '0'
