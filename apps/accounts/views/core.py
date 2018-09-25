import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from ..forms import (RequestInviteForm, AccountSettingsForm,
                     LoginForm,
                     SignupForm)
from ..models import *
from ..utils import validate_activation_key
from django.conf import settings

logger = logging.getLogger('sharemyhealth_.%s' % __name__)


def mylogout(request):
    logout(request)
    messages.success(request, _('You have been logged out.'))
    return HttpResponseRedirect(reverse('home'))


@login_required
def account_settings(request):
    name = _('Account Settings')
    up = get_object_or_404(UserProfile, user=request.user)

    groups = request.user.groups.values_list('name', flat=True)
    for g in groups:
        messages.info(request, _('You are in the group: %s' % (g)))

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # update the user info
            request.user.username = data['username']
            request.user.email = data['email']
            request.user.first_name = data['first_name']
            request.user.last_name = data['last_name']
            request.user.save()
            # update the user profile
            up.organization_name = data['organization_name']
            up.create_applications = data['create_applications']
            up.mobile_phone_number = data['mobile_phone_number']
            up.create_applications = data['create_applications']
            up.save()
            messages.success(request,
                             'Your account settings have been updated.')
            return render(request,
                          'account-settings.html',
                          {'form': form, 'name': name})
        else:
            # the form had errors
            return render(request,
                          'account-settings.html',
                          {'form': form, 'name': name})

    # this is an HTTP GET
    form = AccountSettingsForm(
        initial={
            'username': request.user.username,
            'email': request.user.email,
            'organization_name': up.organization_name,
            'mfa_login_mode': up.mfa_login_mode,
            'mobile_phone_number': up.mobile_phone_number,
            'create_applications': up.create_applications,
            'last_name': request.user.last_name,
            'first_name': request.user.first_name,
            'access_key_reset': up.access_key_reset,
        }
    )
    return render(request,
                  'account-settings.html',
                  {'name': name, 'form': form})
