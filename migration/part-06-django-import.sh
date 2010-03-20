#!/bin/sh

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"
export COUCHDB_HOST
export COUCHDB_PORT
export COUCHDB_URL_ROOT

#rm /tmp/memopol2.sqlite

python part-06-django-import.py
