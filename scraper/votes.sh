#!/usr/bin/ksh

[[ -z "$1" ]] && {
    echo "./${0##*/} <20091124>"
    exit
}
f=`mktemp`
curl -qs "http://www.europarl.europa.eu/sides/getDoc.do?pubRef=-//EP//NONSGML+PV+$1+RES-RCV+DOC+WORD+V0//EN&language=EN" >$f
wvHtml $f - | ./votes.py
rm $f
