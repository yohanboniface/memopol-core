#!/usr/bin/python
# -*- coding:Utf-8 -*-

import json

from urllib import urlopen

from django.conf import settings

from meps.models import MEP

from current_meps_json_2_sql import manage_mep, clean

if __name__ == "__main__":
    print "load json"
    print "fetch json from %s" % settings.PARLTRACK_URL +  "/search?s_meps=on&q=+&format=json"
    meps = json.load(urlopen(settings.PARLTRACK_URL + "/search?s_meps=on&q=+&format=json"))
    a = 0
    for mep_json in meps["items"]:
        a += 1
        print a, "-", mep_json["Name"]["full"]
        in_db_mep = MEP.objects.filter(ep_id=mep_json["UserID"])
        if in_db_mep:
            mep = in_db_mep[0]
            manage_mep(mep, mep_json)
    clean()

# vim:set shiftwidth=4 tabstop=4 expandtab:
