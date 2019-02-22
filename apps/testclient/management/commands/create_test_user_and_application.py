from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.fhirproxy.models import Crosswalk
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


def create_group(name="BlueButton"):

    g, created = Group.objects.get_or_create(name=name)
    if created:
        print("%s group created" % (name))
    else:
        print("%s group pre-existing. Create skipped." % (name))
    return g


def create_user(group):

    if User.objects.filter(username="fred").exists():
        User.objects.filter(username="fred").delete()

    u = User.objects.create_user(username="fred",
                                 first_name="Fred",
                                 last_name="Flinstone",
                                 email='fred@example.com',
                                 password="foobarfoobarfoobar",)
    UserProfile.objects.create(user=u)

    u.groups.add(group)
    c, g_o_c = Crosswalk.objects.get_or_create(user=u,
                                               fhir_patient_id=settings.DEFAULT_SAMPLE_FHIR_ID)
    return u


def create_application(user, group):
    Application.objects.filter(name="TestApp").delete()
    redirect_uri = "%s/testclient/callback" % (settings.HOSTNAME_URL)
    if not(redirect_uri.startswith("http://") or redirect_uri.startswith("https://")):
        redirect_uri = "https://" + redirect_uri
    a = Application.objects.create(name="TestApp",
                                   redirect_uris=redirect_uri,
                                   user=user,
                                   client_type="confidential",
                                   authorization_grant_type="authorization-code")

    return a


def create_test_token(user, application):

    now = timezone.now()
    expires = now + timedelta(days=1)
    t = AccessToken.objects.create(user=user, application=application,
                                   token="sample-token-string",
                                   expires=expires)
    return t


class Command(BaseCommand):
    help = 'Create a test user and application for the test client'

    def handle(self, *args, **options):
        g = create_group()
        u = create_user(g)
        a = create_application(u, g)
        t = create_test_token(u, a)
        print("Name:", a.name)
        print("client_id:", a.client_id)
        print("client_secret:", a.client_secret)
        print("access_token:", t.token)
        print("redirect_uri:", a.redirect_uris)
