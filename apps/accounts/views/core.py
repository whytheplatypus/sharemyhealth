import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from ..forms import AccountSettingsForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout


logger = logging.getLogger('sharemyhealth_.%s' % __name__)


def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def account_settings(request):
    name = _('Account Settings')

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
            'last_name': request.user.last_name,
            'first_name': request.user.first_name,
        }
    )
    return render(request,
                  'account-settings.html',
                  {'name': name, 'form': form})
