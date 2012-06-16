#!/usr/bin/python
# -*- coding:Utf-8 -*-

import urllib2
from django.conf import settings

PARLTRACK_URL = settings.PARLTRACK_URL

current_meps = "/meps/?format=json"

def get_data():
    #return urllib2.urlopen(PARLTRACK_URL + current_meps).read()
    #return urllib2.urlopen("http://parltrack.euwiki.org/dumps/ep_meps_current.json").read()
    return urllib2.urlopen("http://parltrack.euwiki.org/dumps/ep_meps2.json").read()

if __name__ == "__main__":
    print "downloading data from %s%s" %(PARLTRACK_URL, current_meps)
    open("meps.json", "w").write(get_data())
    print "onomnomnom, lovely data successfully downloaded"

# vim:set shiftwidth=4 tabstop=4 expandtab:
