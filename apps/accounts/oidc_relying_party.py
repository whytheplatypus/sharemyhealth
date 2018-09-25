from social_core.backends.open_id_connect import OpenIdConnectAuth
from social_core.backends.google import GoogleOAuth2
0
__author__ = "Alan Viars"


class VerifyMyIdentityOpenIdConnect(OpenIdConnectAuth):
    name = 'verifymyidentity-openidconnect'
    OIDC_ENDPOINT = 'http://verifymyidentity:8001'
    # differs from value in discovery document
    # http://openid.net/specs/openid-connect-core-1_0.html#rfc.section.15.6.2
    # ID_TOKEN_ISSUER = 'http://verifymyidentity:8001'
    DEFAULT_SCOPE = ['openid', ]#'profile', 'email']
    #def user_data(self, access_token, *args, **kwargs):
    #    """Return user data from Google API"""
    #    return self.get_json(
    #        'https://www.googleapis.com/plus/v1/people/me/openIdConnect',
    #        params={'access_token': access_token, 'alt': 'json'}
    #    )
