from configuration.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'smsapp',
        'USER': 'smsapp',
        'PASSWORD': 'smsapp',
        'HOST': 'db',
        'PORT': '5432',
    }
}
