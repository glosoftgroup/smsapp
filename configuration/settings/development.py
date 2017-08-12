from .base import *

DEBUG = True
INSTALLED_APPS += ('django_extensions',)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smsapp',
        'USER': 'smsapp',
        'ADMINUSER':'postgres',
        'PASSWORD': 'smsapp',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
