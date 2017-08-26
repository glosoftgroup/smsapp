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

from app_dir.api.models import SmsMessage, Network
from app_dir.api.serializers import MessageSerializer
from app_dir.core import SendAfricasTalking

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

    def get_handler(self, partner):
        partner_handler_name = str.replace(partner, '-', '_')

        try:
            return getattr(self, partner_handler_name)
        except AttributeError:
            raise ValueError('Network endpoint not Implemented.')

    def post(self, request):
        logger = get_logger(__name__)
        logger.info('console_sms_request', request=request.data)

        try:
            # Check if incoming data structure is valid
            serializer = MessageSerializer(data=request.data, many=True)
            if serializer.is_valid():
                # Iterate through the list
                for item in serializer.data:
                    values = dict(item)
                    network, created = Network.objects.get_or_create(
                        name=values.get('partner')
                    )
                    sms_model = SmsMessage(
                        msisdn=values.get('msisdn'),
                        message_id=values.get('message_id'),
                        sender_id=values.get('sender_id', ''),
                        message=values.get('message'),
                        network=network,
                    )
                    sms_model.save()

                    partner = item.get('partner')
                    handler = self.get_handler(partner)
                    handler(
                        sms_message_pk=sms_model.pk,
                        message_details=values
                    )

                    response_content = {"detail": "ok"}
                    response_status = status.HTTP_202_ACCEPTED
                    logger.info(
                        'console_sms_response',
                        response=response_content, status=response_status
                    )

                    return response.Response(
                        response_content, status=response_status
                    )

            else:
                response_status = status.HTTP_400_BAD_REQUEST
                logger.error(
                    'console_sms_response',
                    response=serializer.errors, status=response_status
                )
                response_json = {'detail': serializer.errors}

                return response.Response(response_json, status=response_status)
        except Exception as e:
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            logger.error(
                'console_sms_response', response=str(e), status=response_status
            )

            return response.Response(
                "Internal Server Error", status=response_status
            )

    def tigo_tz(self, sms_message_pk, message_details):

        logger = get_logger(__name__)
        logger.info('talk to africas talking ...')
        correlation_id = str(uuid.uuid4())

        # call queue mechanism, determine what backend frame to use to send sms.
        resp = sendAfricasTalking.sendafricastalkingsms(self)

        response_content = resp
        response_status = status.HTTP_200_ACCEPTED
        logger.info(
            'africas talking response',
            response=response_content, status=response_status
        )
