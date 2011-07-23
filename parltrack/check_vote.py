#!/usr/bin/python
# -*- coding:Utf-8 -*-

import sys
from urllib import urlopen
from json import loads

from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.votes.models import RecommendationData

def check_recommendationdata(object_id):
    rd = get_object_or_404(RecommendationData, id=object_id)
    data  = loads(rd.data)
    meps = map(lambda x: x ["orig"], reduce(lambda a, b: a + b, [i['votes'] for i in data["Abstain"]["groups"] + data["Against"]["groups"] + data["For"]["groups"]]))
    fail = []
    a = 1
    good = True
    for mep in meps:
        mep = mep.replace(u"ß", "SS")
        if urlopen(settings.PARLTRACK_URL + "/mep/%s?format=json&date=%s" % (mep.encode("Utf-8"), rd.date.strftime("%Y-%m-%d"))).code != 200:
            good = False
            fail.append(mep)
            sys.stdout.write("Didn't managed to find this mep: %s\n" % mep.encode("Utf-8"))
            sys.stdout.flush()
        sys.stdout.write("%i/%i\r" % (a, len(meps)))
        sys.stdout.flush()
        a += 1
    print
    print "end"
    return fail

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >>sys.stderr, "You need to give me the id of a recommendationdata"
        sys.exit(1)
    check_recommendationdata(int(sys.argv[1]))

# vim:set shiftwidth=4 tabstop=4 expandtab:
