from collections import OrderedDict
# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, renderers
from rest_framework_xml.renderers import XMLRenderer

import os


class CDAExample(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer, XMLRenderer, )

    def get_data(self):
        data = OrderedDict()
        data["sub"] = "12345678912345"
        data["patient"] = "984848940"
        with open(os.path.join(os.path.dirname(__file__), "sample-cda.xml")) as f:
            ccda = f.read()
            data["cda"] = ccda
        return data

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        return Response(self.get_data())
