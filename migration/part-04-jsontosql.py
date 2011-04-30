#!/usr/bin/python

import json
import sys
import os

#sys.path += os.path.join(os.path.realpath(os.path.curdir
sys.path += ["/home/psycojoker/code/django/sqlmemopol2/apps/"]
sys.path += ["/home/psycojoker/code/django/sqlmemopol2/"]

from meps.models import Deleguation, Committe, Country, Group, Opinion

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
    print " * remove Group"
    Group.objects.all().delete()
    print " * remove Opinion"
    Opinion.objects.all().delete()

def _create_functions(functions):
    for function in functions:
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

def _create_countries(country):
    if not Country.objects.filter(code=country["code"]):
        print "   new country: %s (%s)" % (country["name"], country["code"])
        Country.objects.create(code=country["code"], name=country["name"])

def _create_groups(group):
    if not Group.objects.filter(abbreviation=group["abbreviation"]):
        print "   new group: %s (%s)" % (group["name"], group["abbreviation"])
        Group.objects.create(abbreviation=group["abbreviation"], name=group["name"])

def _create_opinions(opinions):
    for opinion in opinions:
        if not Opinion.objects.filter(title=opinion["title"]):
            print "    new opinion:", opinion["title"]
            Opinion.objects.create(title=opinion["title"], content=opinion["content"], url=opinion["url"])


def manage_meps(path):
    print "Load meps json."
    meps = json.loads(open(os.path.join(path, MEPS), "r").read())
    print "Create Committe and Deleguation:"
    a = 0
    for mep in meps:
        a += 1
        print " *", a
        _create_functions(mep["functions"])
        _create_countries(mep["infos"]["constituency"]["country"])
        _create_groups(mep["infos"]["group"])
        _create_opinions(mep["opinions"])

if __name__ == "__main__":
    path = sys.argv[1]
    clean()
    manage_meps(path)

