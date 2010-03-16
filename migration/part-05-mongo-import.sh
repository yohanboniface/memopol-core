#!/bin/sh

set -e

source ./env

for i in $XML_DUMPS_PATH/*xml.json; do

  coll=$(basename $i | cut -d'.' -f1)
  mongoimport --host $MONGO_HOST:$MONGO_PORT --username ""$MONGO_USER --password ""$MONGO_PASSWORD -d $MONGO_DB_NAME --drop -c $coll $i

done


