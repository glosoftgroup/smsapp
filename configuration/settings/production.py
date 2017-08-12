# flake8:noqa
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
STAGE = "production"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smsapp',
        'USER': 'smsappuser',
        'ADMINUSER':'postgres',
        'PASSWORD': '38kzddvSgRWjQXsMj9',
        'HOST': 'smsapp-production.cjlbpfelubaj.eu-west-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    # ...
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': 'https://5fa65a7464454dcbadff8a7587d1eaa0:205b12d200e24b39b4c586f7df3965ba@app.getsentry.com/29978',
}

CONSUL_HOST = "http://internal-hermes-consul-alb-369461576.eu-west-1.elb.amazonaws.com/v1/kv/"
SLACK_NOTIFICATION_ENABLED = False