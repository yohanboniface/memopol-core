#!/usr/bin/python

import json
import sys
import os

from datetime import date

#sys.path += os.path.join(os.path.realpath(os.path.curdir
sys.path += ["/home/psycojoker/code/django/sqlmemopol2/apps/"]
sys.path += ["/home/psycojoker/code/django/sqlmemopol2/"]

from meps.models import Deleguation, Committe, Country, Group, Opinion, Mep, Email

MEPS = "meps.xml.json"
MPS = "mps.xml.json"
VOTES = "votes.xml.json"

def clean():
    print "Clean database:"
    print " * remove Mep"
    Mep.objects.all().delete()
    print " * remove Email"
    Email.objects.all().delete()
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

def _create_mep(mep):
    name = mep["infos"]["name"]
    birth_date = mep["infos"]["birth"]["date"]
    Mep.objects.create(key_name=name["wiki"],
                       first_name=name["first"],
                       last_name=name["last"],
                       full_name=name["full"],
                       gender=mep["infos"]["gender"],
                       picture=mep["infos"]["picture"],
                       birth_place=mep["infos"]["birth"]["place"]["city"],
                       birth_date=date(int(birth_date["year"]), int(birth_date["month"]), int(birth_date["day"])),
                       ep_id=mep["extid"],
                       ep_opinions=mep["activities"]["opinions"],
                       ep_debates=mep["activities"]["debates"],
                       ep_questions=mep["activities"]["questions"],
                       ep_declarations=mep["activities"]["declarations"],
                       ep_reports=mep["activities"]["reports"],
                       ep_motions=mep["activities"]["motions"],
                       ep_webpage=mep["contact"]["web"][0]["text"])

    if type(mep["contact"]["email"]) is list:
        for email in mep["contact"]["email"]:
            print "   new email", email
            Email.objects.create(email=email)
    else:
        print "   new email", mep["contact"]["email"]["text"]
        Email.objects.create(email=mep["contact"]["email"]["text"])

def manage_meps(path):
    print "Load meps json."
    meps = json.loads(open(os.path.join(path, MEPS), "r").read())
    print "Create Committe and Deleguation:"
    a = 0
    for mep in meps:
        if mep["_id"] in ["LucasHartong", "InnocenzoLeontini"]:
            # rubish data
            continue
        a += 1
        print " *", a, "-", mep["infos"]["name"]["full"], "-", mep["_id"]
        _create_functions(mep["functions"])
        _create_countries(mep["infos"]["constituency"]["country"])
        _create_groups(mep["infos"]["group"])
        _create_opinions(mep["opinions"])
        _create_mep(mep)

if __name__ == "__main__":
    path = sys.argv[1]
    clean()
    manage_meps(path)

