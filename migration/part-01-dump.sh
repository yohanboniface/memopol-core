#!/bin/bash
# dump dbxml data to xml files

set -e

source ./env

test -x "$DBXML_BINARY" || (echo "Incorrect DBXML_BINARY [$DBXML_BINARY]" && exit 1)
test -d "$DBXML_DATA_PATH"  || (echo "Incorrect DBXML_DATA_PATH [$DBXML_DATA_PATH]" && exit 1)
mkdir -p "$XML_DUMPS_PATH"  || (echo "Cannot create XML_DUMPS_PATH [$XML_DUMPS_PATH]" && exit 1)


t=$(tempfile) || exit
trap "rm -f -- '$t'" EXIT

cat >$t <<_EOF_
openContainer meps.dbxml
cquery '*'
print $XML_DUMPS_PATH/dump-meps.xml

openContainer mps.dbxml
cquery '*'
print $XML_DUMPS_PATH/dump-mps.xml

openContainer votes.dbxml
cquery '*'
print $XML_DUMPS_PATH/dump-votes.xml

quit
_EOF_


echo "Running dbxml dump script..."
$DBXML_BINARY -h $DBXML_DATA_PATH -s $t || (echo "Failed running dbxml script" && exit 1)

exit 0
