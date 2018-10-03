from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


def authenticated_home(request):
    if request.user.is_authenticated:
        name = _('Authenticated Home')
        try:
            profile = request.user.userprofile
        except Exception:
            profile = None

        # this is a GET
        context = {'name': name, 'profile': profile}
        template = 'authenticated-home.html'
    else:
        name = ('home')
        context = {'name': name}
        template = 'index.html'
    return render(request, template, context)
