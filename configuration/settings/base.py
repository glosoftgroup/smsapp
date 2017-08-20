"""
Django settings for farmer_feedback project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import structlog
import logging
import logging.config
from django.conf import global_settings

from loglib.logging import KeyValueRenderer
import os

# from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ybu_u+ql8hh@7x51rusm-*7w@983kx%l0yx6l^28(j%ir4p^%('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STAGE = "development"

ALLOWED_HOSTS = ["*"]

ADMINS = (
    ('marete kent', 'maretekent@gmail.com'),

)
CORS_ORIGIN_ALLOW_ALL = True

# Application definition
DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
)

THIRD_PARTY_APPS = (
    'gunicorn',
)

LOCAL_APPS = (
    'utilities',
    'loglib',
)

# maintain the given order, because we want the post-migrate signal for our local app('hermes_status')
# to run before those of 'django.contrib.admin', otherwise you'll get an error.
INSTALLED_APPS = LOCAL_APPS + DEFAULT_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
            "debug": DEBUG
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

ROOT_URLCONF = 'configuration.urls'

WSGI_APPLICATION = 'configuration.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'static'))

STATIC_URL = '/static/'
S3_BUCKET = ''
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''

# MEDIA_URL = 'https://{0}/kenblest/kenblestkenya/attachments/'.format(conn.server_name())
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TIME_ZONE = 'Africa/Nairobi'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'environment': {
            '()': 'utilities.logging_filter.CustomFilter',
        },
    },
    'handlers': {
        'debug_logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/debug.log',
            'formatter': 'verbose'
        },
        'error_logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log/error.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s module=%(module)s, '
                      'process_id=%(process)d, %(message)s'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'error_logfile'],
            'level': 'ERROR',
        },
        'api': {
            'handlers': ['console', 'debug_logfile'],
            'level': 'DEBUG',
        },
        'smsapp': {
            'handlers': ['console', 'debug_logfile'],
            'level': 'DEBUG',
        },
        'app_dir': {
            'handlers': ['console', 'debug_logfile'],
            'level': 'DEBUG',
            'propagate': False
        },
        'utilities': {
            'handlers': ['console', 'debug_logfile'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

structlog.configure(
    logger_factory=structlog.stdlib.LoggerFactory(),
    processors=[
        structlog.processors.UnicodeEncoder(),
        KeyValueRenderer(),
    ]
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# api key that Console needs to use to call Hermes-sms
DEFAULT_CUSTOM_API_KEY = 'B+XXazAET/ZGVmYXVsdHN0cm9uZ2tleWZvcnRoZWFwaQ=='

API_KEY = "26un912GIXzK95x9eq8u398u2"
SLACK_NOTIFICATION_WEBHOOK_URL= "https://hooks.slack.com/services/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"

CONSUL_HOST = "http://10.0.0.11:8500/v1/kv/"
CONSUL_REQUEST_TIMEOUT=10

SLACK_NOTIFICATION_DEFAULT_BOT_NAME = 'hermes-bot'
SLACK_NOTIFICATION_DEFAULT_CHANNEL = '#queue'
SLACK_NOTIFICATION_TEMPLATE = "The queue {queue} of {service} is now {status}"
SLACK_NOTIFICATION_ENABLED = True
