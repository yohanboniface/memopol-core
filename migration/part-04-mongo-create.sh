#!/bin/sh

set -e

source ./env


t=$(tempfile)".js" || exit
trap "rm -f -- '$t'" EXIT

cat >$t <<_EOF_
db.createCollection("meps");
db.createCollection("mps");
db.createCollection("votes");
_EOF_

cat $t


mongo --host $MONGO_HOST --port $MONGO_PORT --username ""$MONGO_USER --password ""$MONGO_PASSWORD $MONGO_DB_NAME $t
