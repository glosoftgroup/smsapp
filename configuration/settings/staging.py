# flake8:noqa
from .base import *

DEBUG = False

STAGE = "staging"

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smsapp',
        'USER': 'smsappuser',
        'ADMINUSER':'postgres',
        'PASSWORD': 'Y904510P6cXM668mO96e',
        'HOST': 'smsapp-staging.cjlbpfelubaj.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    # ...
    'raven.contrib.django.raven_compat',
    # 'debug_toolbar',
    # 'django_extensions',
)

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
CONSUL_HOST = "http://consul-service-alb-665250589.eu-west-1.elb.amazonaws.com/v1/kv/"
SLACK_NOTIFICATION_ENABLED = False
