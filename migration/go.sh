#!/bin/bash

source ./env

if ! test -z "$ENV_HAS_NOT_BEEN_EDITED"; then
 echo "Please review and correct environment settings first !"
 exit 1
fi

for i in part-*.sh; do

 echo "Running [$i]"
 /bin/bash $i
 if test $? -ne 0; then
   echo "Script [$i] failed, stopping..."
   exit 1
 fi
 
done
