from django.conf import settings

from rest_framework import exceptions
from rest_framework import authentication
from rest_framework import status

from structlog import get_logger


class KeyAuth(authentication.BaseAuthentication):
    """
    Custom authentication class according to Header Token
    """
    api_key = settings.DEFAULT_CUSTOM_API_KEY

    def authenticate(self, request):
        logger = get_logger(__name__)

        try:
            incoming_api_key = request.META['HTTP_APIKEY']

        except (AttributeError, KeyError):  # Missing Authorization Header
            logger.error(
                'authentication_response', response="missing api key",
                status=status.HTTP_401_UNAUTHORIZED
            )

            logger.debug('authentication_response', response=request,
                         status=status.HTTP_401_UNAUTHORIZED)
            raise exceptions.AuthenticationFailed('Unauthorised')
        else:
            if incoming_api_key != self.api_key:
                logger.error(
                    'authentication_response', response="invalid api key",
                    status=status.HTTP_401_UNAUTHORIZED
                )
                raise exceptions.AuthenticationFailed()
            else:
                return None, incoming_api_key
