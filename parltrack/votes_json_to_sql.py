#!/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import sys
from dateutil.parser import parse
from json import loads, dumps

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("parltrack")] + "apps/"]

from votes.models import RecommendationData
from django.db import transaction

if __name__ == "__main__":
    print "cleaning"
    RecommendationData.objects.all().delete()
    print "read file"
    current_json = ""
    a = 1
    with transaction.commit_on_success():
        for i in open("ep_votes.json", "r"):
            if i in ("[{\n", "{\n"):
                #print "begin doc"
                current_json += "{\n"
            elif "}\n" == i:
                #print "end"
                current_json += "\n}"
                vote = loads(current_json)
                RecommendationData.objects.create(proposal_name=vote.get("report", vote["title"]),
                                                 title=vote["title"],
                                                 data=dumps(vote, indent=4),
                                                 date=parse(vote["ts"])),
                current_json = ""
                sys.stdout.write("%s\r" % a)
                sys.stdout.flush()
                a += 1
            elif i == ",\n":
                pass
            else:
                current_json += i
        sys.stdout.write("\n")

# vim:set shiftwidth=4 tabstop=4 expandtab:
