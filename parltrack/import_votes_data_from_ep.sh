#!/bin/bash

export PYTHONPATH="../:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

echo "[downloading EP votes data file]"
wget -O ep_votes.json http://parltrack.euwiki.org/dumps/ep_votes.json
echo "[importing data into the database]"
python ./votes_json_to_sql.py || (echo "import json data into the database failed" && echo "end" && exit 1)

echo
echo "successful end"
