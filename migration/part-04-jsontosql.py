#!/usr/bin/python

import json
import sys
import os

#sys.path += os.path.join(os.path.realpath(os.path.curdir
sys.path += ["/home/psycojoker/code/django/sqlmemopol2/apps/"]
sys.path += ["/home/psycojoker/code/django/sqlmemopol2/"]

from meps.models import Deleguation, Committe, Country

MEPS = "meps.xml.json"
MPS = "mps.xml.json"
VOTES = "votes.xml.json"

def clean():
    print "Clean database:"
    print " * remove Deleguation"
    Deleguation.objects.all().delete()
    print " * remove Committe"
    Committe.objects.all().delete()
    print " * remove Country"
    Country.objects.all().delete()

def manage_meps(path):
    print "Load meps json."
    meps = json.loads(open(os.path.join(path, MEPS), "r").read())
    print "Create Committe and Deleguation:"
    a = 0
    for mep in meps:
        a += 1
        print " *", a
        for function in mep["functions"]:
            try:
                if function.get("abbreviation") and not Committe.objects.filter(name=function["label"], abbreviation=function["abbreviation"]):
                    print "   new committe:", function["abbreviation"], "-", function["label"]
                    Committe.objects.create(abbreviation=function["abbreviation"],
                                            name=function["label"])
                elif type(function["label"]) is unicode and not Deleguation.objects.filter(name=function["label"]):
                    print "   new deleguation:", function["label"]
                    Deleguation.objects.create(name=function["label"])
                elif type(function["label"]) is not unicode and not Deleguation.objects.filter(name=function["label"]["text"]):
                    print "   new deleguation:", function["label"]["text"]
                    Deleguation.objects.create(name=function["label"]["text"])
                else:
                    pass
            except KeyError, e:
                print function
                raise e

        country = mep["infos"]["constituency"]["country"]
        if not Country.objects.filter(code=country["code"]):
            print "   new country: %s (%s)" % (country["name"], country["code"])
            Country.objects.create(code=country["code"], name=country["name"])

if __name__ == "__main__":
    path = sys.argv[1]
    clean()
    manage_meps(path)

