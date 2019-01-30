from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from jwkest.jwt import JWT

_author_ = "Alan Viars"


def authenticated_home(request):
    if request.user.is_authenticated:

        try:
            vmi = request.user.social_auth.filter(
                provider='verifymyidentity-openidconnect')[0]
            extra_data = vmi.extra_data
            if 'id_token' in vmi.extra_data.keys():
                id_token = extra_data.get('id_token')
                parsed_id_token = JWT().unpack(id_token)
                parsed_id_token = parsed_id_token.payload()

        except Exception:
            id_token = "No ID token."
            parsed_id_token = "No ID token."

        name = _('Authenticated Home')
        try:
            profile = request.user.userprofile
        except Exception:
            profile = None

        # this is a GET
        context = {'name': name, 'profile': profile,
                   'id_token': id_token,
                   'id_token_payload': parsed_id_token}

        template = 'authenticated-home.html'
    else:
        name = ('home')
        context = {'name': name}
        template = 'index.html'
    return render(request, template, context)
