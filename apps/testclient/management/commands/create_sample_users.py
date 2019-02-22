from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.fhirproxy.models import Crosswalk
import csv


def create_group(name="BlueButton"):

    g, created = Group.objects.get_or_create(name=name)
    if created:
        print("%s group created" % (name))
    else:
        print("%s group pre-existing. Create skipped." % (name))
    return g


def create_user(group, row):
    User = get_user_model()
    if User.objects.filter(username=row["username"]).exists():
        User.objects.filter(username=row["username"]).delete()

    u = User.objects.create_user(username=row["username"],
                                 first_name=row["first_name"],
                                 last_name=row["last_name"],
                                 email=row["email"],
                                 password=row["password"])
    UserProfile.objects.create(user=u)

    u.groups.add(group)
    c, g_o_c = Crosswalk.objects.get_or_create(user=u,
                                               fhir_id=row["patient"])
    return u


class Command(BaseCommand):
    help = 'Create a test user and application for the test client'

    def add_arguments(self, parser):
        parser.add_argument('--accounts_file', dest='accounts_file',
                            nargs='?', help="The CSV containing the accounts info.",
                            default='apps/testclient/fixtures/sample_accounts.csv')

    def handle(self, *args, **kwargs):
        g = create_group()

        # number of accounts counter
        accounts_counter = 0

        # process CSV
        with open(kwargs['accounts_file']) as csvfile:
            reader = csv.DictReader(csvfile)
            print("Loading Test Users...")
            for row in reader:
                accounts_counter += 1
                u = create_user(g, row)
                print("User", u.username, "created.")
        print("Complete!")
