#!/bin/bash

set -e

source ./env

for i in $XML_DUMPS_PATH/*xml; do

  ./part-03-xmltojson.py $i $i".json"

done


