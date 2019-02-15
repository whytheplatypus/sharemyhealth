from django.http import JsonResponse, HttpResponse
from collections import OrderedDict
# from django.shortcuts import render
import os


def cda_in_json(request):
    od = OrderedDict()
    od["sub"] = "12345678912345"
    od["patient"] = "984848940"
    fp = os.path.join(os.path.dirname(__file__), "sample-cda.xml")
    od["cda"] = open(fp).read()
    return JsonResponse(od)


def cda_as_xml(request):
    fp = os.path.join(os.path.dirname(__file__), "sample-cda.xml")
    return HttpResponse(open(fp).read(), content_type='text/xml')
