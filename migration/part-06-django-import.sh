#!/bin/bash

source ./env

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"
export COUCH_HOST
export COUCH_PORT
export COUCH_URL_ROOT

# if we're using virtualenvwrapper, create the sqlite db there
if ! test -z $VIRTUAL_ENV; then
  SQLITE_FILE=$VIRTUAL_ENV/memopol2.sqlite
else
  SQLITE_FILE=/tmp/$USER-memopol2.sqlite
fi

# if a previous sqlite file exist, move it out of the way
if test -f $SQLITE_FILE; then
  mv $SQLITE_FILE $SQLITE_FILE$(date +%s)
fi

cd ../memopol2
./manage.py syncdb
cd -

python part-06-django-import.py
