#!/bin/sh

source ./env

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"
export COUCH_HOST
export COUCH_PORT
export COUCH_URL_ROOT

if ! test -f /tmp/memopol2.sqlite; then
  cd ../memopol2
  ./manage.py syncdb
  cd -
fi


python part-06-django-import.py
