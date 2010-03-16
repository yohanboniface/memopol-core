#!/bin/sh

set -e

source ./env

for i in $XML_DUMPS_PATH/*xml; do

  python xml-to-json.py $i $i".json"

done


