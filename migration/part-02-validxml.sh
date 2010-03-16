#!/bin/sh
# Add xml header with encoding and a top level container tag

set -e

source ./env

for i in $XML_DUMPS_PATH/*xml; do

(echo '<?xml version="1.0" encoding="UTF-8" ?>' && echo '<dump>' && cat $i && echo "</dump>" ) > $i".2"
mv $i".2" $i

done
