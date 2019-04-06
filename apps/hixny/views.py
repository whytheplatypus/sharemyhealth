# import logging #TODO
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..accounts.models import UserProfile
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from .models import HIXNYProfile
from django.conf import settings
from django.core.files.base import ContentFile

# curl  https://integration.hixny.com:6443/ -k --user
# password-client:20P@55230R419 -d
# "grant_type=password&username=avairsqa&password=sector7g&scope=/PHRREGISTER"


@login_required
def get_authorization(request):

    up, g_o_c = UserProfile.objects.get_or_create(user=request.user)
    hp, g_o_c = HIXNYProfile.objects.get_or_create(user=request.user)
    status = ""
    notice = ""
    r = requests.post(
        settings.HIXNY_TOKEN_API_URI,
        data={
            "grant_type": "password",
            "username": settings.HIXNY_WORKBENCH_USERNAME,
            "password": settings.HIXNY_WORKBENCH_PASSWORD,
            "scope": "/PHRREGISTER"},
        verify=False,
        auth=HTTPBasicAuth(
            'password-client',
            settings.HIXNY_BASIC_AUTH_PASSWORD))
    response_json = r.json()
    access_token = response_json['access_token']
    access_token_bearer = "Bearer %s" % (access_token)
    # print("AT", access_token)
    hp.step_1 = True
    hp.save()
    # oas = OAuth2Session(token=access_token)
    # userinfo = oas.get(userinfo_uri).json(object_pairs_hook=OrderedDict)

    patient_search_xml = """
                        <PatientSearchPayLoad>
                        <PatGender>%s</PatGender>
                        <PatDOB>%s</PatDOB>
                        <PatFamilyName>%s</PatFamilyName>
                        <PatGivenName>%s</PatGivenName>
                        <PatMiddleName></PatMiddleName>
                        <PatPrefix></PatPrefix>
                        <PatSuffix></PatSuffix>
                        <PatAddrStreetOne></PatAddrStreetOne>
                        <PatAddrStreetTwo></PatAddrStreetTwo>
                        <PatAddrCity></PatAddrCity>
                        <PatAddrZip></PatAddrZip>
                        <PatAddrState></PatAddrState>
                        <PatSSN></PatSSN>
                        <PatHomePhone></PatHomePhone>
                        <PatEmail></PatEmail>
                        <WorkBenchUserName>%s</WorkBenchUserName>
                        </PatientSearchPayLoad>
                        """ % (up.gender_intersystems,
                               up.birthdate_intersystems,
                               up.user.last_name, up.user.first_name,
                               settings.HIXNY_WORKBENCH_USERNAME)
    # print(patient_search_xml)
    response2 = requests.post(settings.HIXNY_PHRREGISTER_API_URI,
                              verify=False,
                              headers={'Content-Type': 'application/xml',
                                       'Authorization': access_token_bearer},
                              data=patient_search_xml
                              )

    f = ET.XML(response2.content)

    for element in f:
        print("ELEMENT", element)
        for e in element.getchildren():
            print(e)
            if e.tag == "{urn:hl7-org:v3}Status":
                status = e.text
            if e.tag == "{urn:hl7-org:v3}Notice":
                notice = e.text

            if e.tag == "{urn:hl7-org:v3}TERMSACCEPTED":
                hp.terms_accepted = e.text
            if e.tag == "{http://www.intersystems.com/hs/portal/enrollment}TermsString":
                hp.terms_string = e.text
            if e.tag == "{urn:hl7-org:v3}StageUserPassword":
                hp.stageuser_password = e.text
            if e.tag == "{urn:hl7-org:v3}StageUserToken":
                hp.stageuser_token = e.text
        hp.save()
        if hp.stageuser_password and hp.stageuser_token:
            hp.step_2 = True
            hp.save()

    # Send the terms accepted response...

    context = {"hp": hp,
               "response1": r,
               "response2": response2,
               "status": status,
               "notice": notice}

    return render(request, 'hixny-user-agreement.html', context)


@login_required
def approve_authorization(request):

    up, g_o_c = UserProfile.objects.get_or_create(user=request.user)
    hp, g_o_c = HIXNYProfile.objects.get_or_create(user=request.user)
    status = ""
    notice = ""
    r = requests.post(
        settings.HIXNY_TOKEN_API_URI,
        data={
            "grant_type": "password",
            "username": settings.HIXNY_WORKBENCH_USERNAME,
            "password": settings.HIXNY_WORKBENCH_PASSWORD,
            "scope": "/PHRREGISTER"},
        verify=False,
        auth=HTTPBasicAuth(
            'password-client',
            settings.HIXNY_BASIC_AUTH_PASSWORD))
    response_json = r.json()
    access_token = response_json['access_token']
    access_token_bearer = "Bearer %s" % (access_token)
    # print("AT", access_token)
    hp.step_1 = True
    hp.save()
    # oas = OAuth2Session(token=access_token)
    # userinfo = oas.get(userinfo_uri).json(object_pairs_hook=OrderedDict)

    activate_xml = """
                <ACTIVATESTAGEDUSERPAYLOAD>
                <DOB>%s</DOB>
                <TOKEN>%s</TOKEN>
                <PASSWORD>%s</PASSWORD>
                <TERMSACCEPTED>%s</TERMSACCEPTED>
                </ACTIVATESTAGEDUSERPAYLOAD>
                """ % (up.birthdate_intersystems,
                       hp.stageuser_token,
                       hp.stageuser_password,
                       hp.consent_to_share_data)
    print(activate_xml)
    response3 = requests.post(settings.HIXNY_ACTIVATESTAGEDUSER_API_URI,
                              verify=False,
                              headers={'Content-Type': 'application/xml',
                                       'Authorization': access_token_bearer},
                              data=activate_xml)

    f = ET.XML(response3.content)
    for element in f:
        print("ELEMENT", element)
        for e in element.getchildren():
            print(e)
            if e.tag == "{urn:hl7-org:v3}ActivatedUserMrn":
                hp.mrn = e.text
                hp.step_3 = True
                hp.save()

    consumer_directive_xml = """
        <CONSUMERDIRECTIVEPAYLOAD>
        <MRN>%s</MRN>
        <DOB>%s</DOB>
        <DATAREQUESTOR>%s</DATAREQUESTOR>
        <CONSENTTOSHAREDATA>%s</CONSENTTOSHAREDATA>
        </CONSUMERDIRECTIVEPAYLOAD>
        """ % (hp.mrn,  up.birthdate_intersystems, hp.data_requestor, hp.consent_to_share_data)
    print(consumer_directive_xml)

    response4 = requests.post(settings.HIXNY_CONSUMERDIRECTIVE_API_URI,
                              verify=False,
                              headers={'Content-Type': 'application/xml',
                                       'Authorization': access_token_bearer},
                              data=consumer_directive_xml)

    print("Consumer Directive response")
    f = ET.XML(response4.content)
    for element in f:
        print("ELEMENT", element)
        if element.tag == "{urn:hl7-org:v3}Status":
            status = element.text
        if element.tag == "{urn:hl7-org:v3}Notice":
            notice = element.text

    response5 = None
    print("STATUS", status, notice)
    if status == "OK":
        hp.step_4 = True
        hp.save()
        print(notice)
        if notice in ("Document has been prepared.",
                      "Document already exists."):

            get_document_payload_xml = """<GETDOCUMENTPAYLOAD>
                                          <MRN>%s</MRN>
                                          <DATAREQUESTOR>%s</DATAREQUESTOR>
                                          </GETDOCUMENTPAYLOAD>
                            """ % (hp.mrn, hp.data_requestor)

            response5 = requests.post(
                settings.HIXNY_GETDOCUMENT_API_URI,
                verify=False,
                headers={
                    'Content-Type': 'application/xml',
                    'Authorization': access_token_bearer},
                data=get_document_payload_xml)

            f = ET.XML(response5.content)
            hp.cda_content = response5.content
            hp.save()
            fn = "%s.xml" % (up.subject)
            hp.cda_file.save(fn, ContentFile(response5.content))
            hp.step_5 = True
            hp.save()

    # Send the terms accepted response...

    context = {"response1": r,
               "response3": response3,
               "response4": response4,
               "response5": response5,
               "hp": hp}

    return render(request, 'hixny-approve-agreement.html', context)
