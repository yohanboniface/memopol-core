#!/bin/bash

export PYTHONPATH="../:"$PYTHONPATH
export PYTHONPATH="../apps/:"$PYTHONPATH
export DJANGO_SETTINGS_MODULE="memopol2.settings"

python import_opinions.py
