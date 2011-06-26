#!/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import sys
import json

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("parltrack")] + "apps/"]

from meps.models import MEP

current_meps = "meps.json"

if __name__ == "__main__":
    print "load json"
    meps = json.load(open(current_meps, "r"))
    new = 0
    to_update = 0
    for mep in meps["meps"]:
        in_db_mep = MEP.objects.filter(ep_id=mep["UserID"])
        if not in_db_mep:
            new += 1
        else:
            to_update += 1
    print "%i new meps, %i meps to update" % (new, to_update)

# vim:set shiftwidth=4 tabstop=4 expandtab:
