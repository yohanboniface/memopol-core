#!/bin/sh

set -e

source ./env

for i in $XML_DUMPS_PATH/*xml; do

  ./xml-to-json.py $i $i".json"

done


