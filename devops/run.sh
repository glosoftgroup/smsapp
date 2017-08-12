#!/usr/bin/env bash

python manage.py migrate --noinput --settings=$DJANGO_SETTINGS_MODULE
python manage.py createcachetable smsapp_cache
python manage.py createcachetable request_cache
python manage.py collectstatic --noinput

# create superuser
#python manage.py init_super_user --settings=$DJANGO_SETTINGS_MODULE
echo "from django.contrib.auth.models import User; User.objects.filter(username='$DEV_LOGIN_USERNAME').exists() or User.objects.create_superuser('$DEV_LOGIN_USERNAME', '$DEV_LOGIN_EMAIL', '$DEV_LOGIN_PASSWORD')" | python manage.py shell --settings=$DJANGO_SETTINGS_MODULE


# debugging with default server uncomment this and comment the gunicorn one
python manage.py runserver 0.0.0.0:8000 --settings=$DJANGO_SETTINGS_MODULE