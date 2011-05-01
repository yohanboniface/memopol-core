#!/usr/bin/python

import json
import sys
import os

from datetime import date, datetime

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("migration")] + "apps/"]

from meps.models import Deleguation, Committe, Country, Group, Opinion, MEP, Email, CV, Party, WebSite, DeleguationRole, CommitteRole, OpinionMEP

MEPS = "meps.xml.json"
MPS = "mps.xml.json"
VOTES = "votes.xml.json"

def clean_meps():
    print "Clean database:"
    print " * remove DeleguationRole"
    DeleguationRole.objects.all().delete()
    print " * remove CommitteRole"
    CommitteRole.objects.all().delete()
    print " * remove MEP"
    MEP.objects.all().delete()
    print " * remove Email"
    Email.objects.all().delete()
    print " * remove CV"
    CV.objects.all().delete()
    print " * remove Deleguation"
    WebSite.objects.all().delete()
    print " * remove WebSite"
    Deleguation.objects.all().delete()
    print " * remove Committe"
    Committe.objects.all().delete()
    print " * remove Country"
    Country.objects.all().delete()
    print " * remove Group"
    Group.objects.all().delete()
    print " * remove Party"
    Party.objects.all().delete()
    print " * remove Opinion"
    Opinion.objects.all().delete()

def clean_mps():
    pass

def _create_meps_functions(functions):
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

def _create_groups_and_party(group):
    if not Group.objects.filter(abbreviation=group["abbreviation"]):
        print "   new group: %s (%s)" % (group["name"], group["abbreviation"])
        Group.objects.create(abbreviation=group["abbreviation"], name=group["name"])

    if not Party.objects.filter(name=group["party"]):
        print "   new party:", group["party"]
        Party.objects.create(name=group["party"])

def _create_opinions(opinions, _mep):
    for opinion in opinions:
        if not Opinion.objects.filter(title=opinion["title"]):
            print "    new opinion:", opinion["title"]
            Opinion.objects.create(title=opinion["title"], content=opinion["content"], url=opinion["url"])

        _date = datetime.strptime(opinion["date"], "%d/%m/%Y").date()
        print "   new link to opinion:", _mep.full_name, _date
        OpinionMEP.objects.create(mep=_mep, opinion=Opinion.objects.get(title=opinion["title"]), date=_date)

def _create_mep(mep):
    name = mep["infos"]["name"]
    birth_date = mep["infos"]["birth"]["date"]
    _mep = MEP.objects.create(active=mep["active"],
                       key_name=name["wiki"],
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
                       ep_webpage=mep["contact"]["web"][0]["text"],
                       bxl_building_name=mep["contact"]["address"]["Bruxelles"]["building"]["name"],
                       bxl_building_abbreviation=mep["contact"]["address"]["Bruxelles"]["building"]["abbreviation"],
                       bxl_office=mep["contact"]["address"]["Bruxelles"]["office"],
                       bxl_fax=mep["contact"]["address"]["Bruxelles"]["fax"],
                       bxl_phone1=mep["contact"]["address"]["Bruxelles"]["phone"][0],
                       bxl_phone2=mep["contact"]["address"]["Bruxelles"]["phone"][1],
                       bxl_street=mep["contact"]["address"]["Bruxelles"]["street"],
                       bxl_postcode=mep["contact"]["address"]["Bruxelles"]["postcode"],
                       stg_building_name=mep["contact"]["address"]["Strasbourg"]["building"]["name"],
                       stg_building_abbreviation=mep["contact"]["address"]["Strasbourg"]["building"]["abbreviation"],
                       stg_office=mep["contact"]["address"]["Strasbourg"]["office"],
                       stg_fax=mep["contact"]["address"]["Strasbourg"]["fax"],
                       stg_phone1=mep["contact"]["address"]["Strasbourg"]["phone"][0],
                       stg_phone2=mep["contact"]["address"]["Strasbourg"]["phone"][1],
                       stg_street=mep["contact"]["address"]["Strasbourg"]["street"],
                       stg_postcode=mep["contact"]["address"]["Strasbourg"]["postcode"],
                       party=Party.objects.get(name=mep["infos"]["group"]["party"]),
                       group_role=mep["infos"]["group"]["role"],
                       group=Group.objects.get(abbreviation=mep["infos"]["group"]["abbreviation"]),
                       country=Country.objects.get(code=mep["infos"]["constituency"]["country"]["code"]))

    if type(mep["contact"]["email"]) is list:
        for email in mep["contact"]["email"]:
            print "   new email", email
            Email.objects.create(email=email, mep=_mep)
    else:
        print "   new email", mep["contact"]["email"]["text"]
        Email.objects.create(email=mep["contact"]["email"]["text"], mep=_mep)

    if mep["contact"]["web"][1:]:
        for i in mep["contact"]["web"][1:]:
            print "   create website:", i["text"]
            WebSite.objects.create(url=i["text"], mep=_mep)

    return _mep

def _create_role(functions, _mep):
    for f in functions:
        if not f.get("abbreviation"):
            name = f["label"] if type(f["label"]) is unicode else f["label"]["text"]
            if not f.get("begin_term"):
                print "   new role in deleguation:", f["role"], "in", name
                DeleguationRole.objects.create(mep=_mep, role=f["role"], deleguation=Deleguation.objects.get(name=name))
            else:
                b = f["begin_term"]
                _begin = date(int(b["year"]), int(b["month"]), int(b["day"]))
                e = f["end_term"]
                _end = date(int(e["year"]), int(e["month"]), int(e["day"]))
                DeleguationRole.objects.create(mep=_mep, role=f["role"], deleguation=Deleguation.objects.get(name=name), begin=_begin, end=_end)
        else:
            if not f.get("begin_term"):
                print "   new role in committe:", f["role"], "in", f["abbreviation"]
                CommitteRole.objects.create(mep=_mep, role=f["role"], committe=Committe.objects.get(abbreviation=f["abbreviation"]))
            else:
                b = f["begin_term"]
                _begin = date(int(b["year"]), int(b["month"]), int(b["day"]))
                e = f["end_term"]
                _end = date(int(e["year"]), int(e["month"]), int(e["day"]))
                CommitteRole.objects.create(mep=_mep, role=f["role"], deleguation=Deleguation.objects.get(name=f["label"]), begin=_begin, end=_end)

def _create_cv(cv, _mep):
    if type(cv) is list:
        for c in cv:
            print "   new cv:", c
            CV.objects.create(title=c, mep=_mep)
    else:
        CV.objects.create(title=cv, mep=_mep)

def manage_meps(path):
    clean_meps()
    print
    print "Load meps json."
    meps = json.loads(open(os.path.join(path, MEPS), "r").read())
    print
    a = 0
    for mep in meps:
        if mep["_id"] in ["LucasHartong", "InnocenzoLeontini"]:
            #rubish data
            continue
        a += 1
        print " *", a, "-", mep["infos"]["name"]["full"], "-", mep["_id"]
        _create_meps_functions(mep["functions"])
        _create_countries(mep["infos"]["constituency"]["country"])
        _create_groups_and_party(mep["infos"]["group"])
        _mep = _create_mep(mep)
        _create_opinions(mep["opinions"], _mep)
        _create_role(mep["functions"], _mep)
        if mep["cv"]:
            _create_cv(mep["cv"]["position"], _mep)

def manage_mps(path):
    clean_mps()
    print
    print "Load mps json."
    mps = json.loads(open(os.path.join(path, MPS), "r").read())
    print
    a = 0
    for mp in mps:
        pass

if __name__ == "__main__":
    path = sys.argv[1]
    manage_meps(path)
    manage_mps(path)

