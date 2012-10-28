#!/bin/bash

export PYTHONPATH="../:"$PYTHONPATH
export PYTHONPATH="../apps/:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

fail()
{
    echo "import json data into the database failed" && echo "end" && exit 1
}

echo "Starting the update"
ipython --pdb ./update_mps.py || fail

echo
echo "successful end"
