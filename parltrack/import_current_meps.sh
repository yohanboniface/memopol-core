#!/bin/bash

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

echo "[download data]"
python get_current_meps_json.py || (echo "getting data failed" && echo "end" && exit 1)
echo "[importing data into the database]"
python ./current_meps_json_2_sql.py || (echo "import json data into the database failed" && echo "end" && exit 1)

echo
echo "successful end"
