#!/bin/bash

source ./env

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"
export COUCH_HOST
export COUCH_PORT
export COUCH_URL_ROOT

if test -f /tmp/memopol2.sqlite; then
  mv /tmp/memopol2.sqlite /tmp/memopol2.sqlite.$(date +%s)
fi

cd ../memopol2
./manage.py syncdb
cd -

python part-06-django-import.py
