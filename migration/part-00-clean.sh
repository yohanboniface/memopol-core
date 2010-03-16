#!/bin/sh

set -e
set -x

source ./env

if test -d $XML_DUMPS_PATH; then

 rm -f $XML_DUMPS_PATH/*.xml
 rm -f $XML_DUMPS_PATH/*.xml.json

 rmdir $XML_DUMPS_PATH

fi