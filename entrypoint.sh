#!/bin/sh
python Source/manage.py migrate
python Source/manage.py makemigrations categories
python Source/manage.py migrate
exec "$@"