#!/bin/bash

export PYTHONPATH="../:"$PYTHONPATH
export PYTHONPATH="../apps/:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

echo "Starting the update"
python ./update_meps.py || (echo "import json data into the database failed" && echo "end" && exit 1)

echo
echo "successful end"
