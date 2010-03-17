#!/bin/sh

set -e

source ./env

for i in meps mps votes; do

 curl -X DELETE $COUCH_URL_ROOT/$i
 curl -X PUT $COUCH_URL_ROOT/$i

done

