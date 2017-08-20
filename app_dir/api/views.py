# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.http import HttpResponse
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework import response
from rest_framework import status
from rest_framework import authentication

from utilities import custom_authentication

from structlog import get_logger

from django.shortcuts import render


# Create your views here.

class MessageRouter(APIView):
    """
    Super Class to Route SMS requests according to Network
    Accepts: JSON Array of JSON Objects
    [
        {
            "msisdn": "255674907064",
            "partner": "tigo-tz",
            "message": "Test Message",
            "priority": "bulk",
            "message_id": "1234",
            "sender_id": "TigoPesa"
        }
    ]
    msisdn              SMS recipient in 12 digit international format
    message_id          Alphanumeric number max length 256
    partner             The mno to which the msisdn belongs
    sender_id(Optional) Message sender
    message             The text to be sent to the customer
    priority            Indicates message type & priority - notification, bulk
    """
    authentication_classes = (
        authentication.SessionAuthentication, custom_authentication.KeyAuth
    )

    def post(self, request):
        logger = get_logger(__name__)
        logger.info('console_sms_request', request=request.data)

        response_content = {"detail": "ok"}
        response_status = status.HTTP_202_ACCEPTED
        logger.info(
            'console_sms_response',
            response=response_content, status=response_status
        )

        return response.Response(
            response_content, status=response_status
        )
