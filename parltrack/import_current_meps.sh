#!/bin/bash

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

python get_current_meps_json.py || (echo "getting data failed" && echo "end" && exit 1)

echo "successful end"
