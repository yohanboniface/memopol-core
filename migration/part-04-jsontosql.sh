#!/bin/bash

set -e

source ./env

export PYTHONPATH="../:"$PYTHONPATH

./part-04-jsontosql.py $XML_DUMPS_PATH
