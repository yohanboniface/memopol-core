#!/bin/bash

set -e

source ./env

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

./part-04-jsontosql.py $XML_DUMPS_PATH
