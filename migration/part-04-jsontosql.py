#!/usr/bin/python

import json
import sys
import os

from datetime import date, datetime

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("migration")] + "apps/"]

from reps.models import WebSite, Party, CV, Email, Opinion, OpinionREP
from meps.models import Deleguation, Committee, Country, Group, MEP, DeleguationRole, CommitteeRole
from mps.models import MP, Function, FunctionMP, Department, Circonscription, Canton, Address, Phone, Mandate
from mps.models import WebSite as _mp_WebSite
from mps.models import Email as _mp_Email
from mps.models import Group as _mp_Group
from votes.models import Vote, SubVote, Result

MEPS = "meps.xml.json"
MPS = "mps.xml.json"
VOTES = "votes.xml.json"

def clean_meps():
    print "Clean meps database:"
    print " * remove DeleguationRole"
    DeleguationRole.objects.all().delete()
    print " * remove CommitteeRole"
    CommitteeRole.objects.all().delete()
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
    print " * remove Committee"
    Committee.objects.all().delete()
    print " * remove Country"
    Country.objects.all().delete()
    print " * remove Group"
    Group.objects.all().delete()
    print " * remove Party"
    Party.objects.all().delete()
    print " * remove Opinion"
    Opinion.objects.all().delete()
    print " * remove OpinionREP"
    OpinionREP.objects.all().delete()

def clean_mps():
    print "Clean mps database:"
    print " * remove FunctionMP"
    FunctionMP.objects.all().delete()
    print " * remove Opinion"
    Opinion.objects.all().delete()
    print " * remove OpinionREP"
    OpinionREP.objects.all().delete()
    print " * remove Group"
    _mp_Group.objects.all().delete()
    print " * remove MP"
    MP.objects.all().delete()
    print " * remove Function"
    Function.objects.all().delete()
    print " * remove WebSite"
    _mp_WebSite.objects.all().delete()
    print " * remove Email"
    _mp_Email.objects.all().delete()
    print " * remove Department"
    Department.objects.all().delete()
    print " * remove Circonscription"
    Circonscription.objects.all().delete()
    print " * remove Canton"
    Canton.objects.all().delete()
    print " * remove Address"
    Address.objects.all().delete()
    print " * remove Phone"
    Phone.objects.all().delete()
    print " * remove Mandate"
    Mandate.objects.all().delete()

def clean_votes():
    print "Clean votes database:"
    print " * remove Vote"
    Vote.objects.all().delete()
    print " * remove SubVote"
    SubVote.objects.all().delete()
    print " * remove Result"
    Result.objects.all().delete()

def _create_meps_functions(functions):
    for function in functions:
        if function.get("abbreviation") and not Committee.objects.filter(name=function["label"], abbreviation=function["abbreviation"]):
            print "   new Committee:", function["abbreviation"], "-", function["label"]
            Committee.objects.create(abbreviation=function["abbreviation"],
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
        OpinionREP.objects.create(mep=_mep, opinion=Opinion.objects.get(title=opinion["title"]), date=_date)

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
                print "   new role in Committee:", f["role"], "in", f["abbreviation"]
                CommitteeRole.objects.create(mep=_mep, role=f["role"], Committee=Committee.objects.get(abbreviation=f["abbreviation"]))
            else:
                b = f["begin_term"]
                _begin = date(int(b["year"]), int(b["month"]), int(b["day"]))
                e = f["end_term"]
                _end = date(int(e["year"]), int(e["month"]), int(e["day"]))
                CommitteeRole.objects.create(mep=_mep, role=f["role"], deleguation=Deleguation.objects.get(name=f["label"]), begin=_begin, end=_end)

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

def _create_mp_opinions(opinions, _mp):
    for opinion in opinions:
        if not Opinion.objects.filter(title=opinion["title"]):
            print "   create new opinion :", opinion["title"]
            Opinion.objects.create(content=opinion["content"], title=opinion["title"], url=opinion["url"])

        if opinion["date"] == "7": #stupid data
            _date = date(2009, 5, 7)
        elif opinion["date"] == "04": #stupid stupid data
            _date = date(2009, 5, 4)
        else:
            try:
                try:
                    _date = datetime.strptime(opinion["date"], "%d/%m/%Y").date()
                except ValueError:
                    _date = datetime.strptime(opinion["date"], "%d/%m/%y").date()
            except ValueError:
                _date = datetime.strptime(opinion["date"], "%m/%Y").date()
        OpinionREP.objects.create(date=_date, mp=_mp, opinion=Opinion.objects.get(title=opinion["title"]))

def _create_mp_functions(mp, _mp):
    for function in mp["functions"]:
        if not Function.objects.filter(title=function["label"]):
            print "   create new", function["type"], ":", function["label"]
            Function.objects.create(type=function["type"], title=function["label"])
        _function = Function.objects.get(title=function["label"])
        FunctionMP.objects.create(function=_function, mp=_mp, role=function["role"], mission=function.get("mission"))

def _create_mp_departments(mp):
    department = mp["infos"]["constituency"]["department"]
    if not Department.objects.filter(number=department["number"]):
        print "   create new department:", department["name"], department["number"]
        Department.objects.create(name=department["name"], number=department["number"])

    if not Circonscription.objects.filter(number=mp["infos"]["constituency"]["number"], department=Department.objects.filter(number=department["number"])):
        print "   create new circonscription:", mp["infos"]["constituency"]["number"]
        Circonscription.objects.create(number=mp["infos"]["constituency"]["number"], department=Department.objects.get(number=department["number"]))

    cantons = mp["infos"]["constituency"]["cantons"]["name"]
    if type(cantons) is not list:
        cantons = cantons.split(";")

    for canton in cantons:
        if not Canton.objects.filter(name=canton, circonscription=Circonscription.objects.get(number=mp["infos"]["constituency"]["number"], department=Department.objects.filter(number=department["number"]))):
            print "   create new canton:", canton
            Canton.objects.create(name=canton, circonscription=Circonscription.objects.get(number=mp["infos"]["constituency"]["number"], department=Department.objects.filter(number=department["number"])))

def _create_mp_groups(group):
    g = group["abbreviation"]
    if not _mp_Group.objects.filter(abbreviation=g):
        print "   new group: %s (%s)" % (group["name"], g)
        _mp_Group.objects.create(abbreviation=g, name=group["name"])

def _create_mp(mp):
    name = mp["infos"]["name"]
    if name["gender"] == "M.":
        name["gender"] = "M"
    elif name["gender"] == "Mme":
        name["gender"] = "M"
    birth_date = mp["infos"]["birth"]["date"]
    _mp = MP.objects.create(active=mp["active"],
                       id=name["wiki"],
                       first_name=name["first"],
                       last_name=name["last"],
                       gender=name["gender"],
                       picture=mp["infos"]["picture"],
                       birth_city=mp["infos"]["birth"]["place"]["city"],
                       birth_department=mp["infos"]["birth"]["place"]["department"],
                       birth_date=date(int(birth_date["year"]), int(birth_date["month"]), int(birth_date["day"])),
                       an_id=mp["extid"],
                       an_speeches=mp["activities"]["speeches"],
                       an_debates=mp["activities"].get("debates", None),
                       an_commissions=mp["activities"]["commissions"],
                       an_reports=mp["activities"]["reports"],
                       an_questions=mp["activities"]["questions"],
                       an_propositions=mp["activities"]["propositions"],
                       an_webpage=mp["contact"]["web"][0]["text"],
                       profession=mp["infos"].get("profession"),
                       department=Department.objects.get(number=mp["infos"]["constituency"]["department"]["number"]),
                       group=_mp_Group.objects.get(abbreviation=mp["infos"]["group"]["abbreviation"]),
                       group_role=mp["infos"]["group"].get("role"))

    if mp["contact"].get("email"):
        if type(mp["contact"]["email"]) is list:
            for email in mp["contact"]["email"]:
                print "   new email", email
                _mp_Email.objects.create(email=email, mp=_mp)
        else:
            print "   new email", mp["contact"]["email"]["text"]
            _mp_Email.objects.create(email=mp["contact"]["email"]["text"], mp=_mp)

    if mp["contact"]["web"][1:]:
        for i in mp["contact"]["web"][1:]:
            print "   create website:", i["text"]
            _mp_WebSite.objects.create(url=i["text"], mp=_mp)

    addrs = mp["contact"]["address"]
    for addr in addrs:
        if addr != "unknown":
            street = addrs[addr]["street"] if type(addrs[addr]["street"]) is unicode else addrs[addr]["street"]["text"]
            print "   new address:", addr, street, addrs[addr]["postcode"]
            _addr = Address.objects.create(key=addr, city=addrs[addr]["city"],
                                   street=street, postcode=addrs[addr]["postcode"], title=addrs[addr].get("label"), mp=_mp)

            if type(addrs[addr].get("phone")) is unicode:
                print "   new phone number:", addrs[addr]["phone"]
                Phone.objects.create(number=addrs[addr]["phone"], type="phone", address=_addr)
            elif type(addrs[addr].get("phone")) is list:
                for phone in addrs[addr].get("phone"):
                    print "   new phone number:", phone
                    Phone.objects.create(number=phone, type="phone", address=_addr)
            if type(addrs[addr].get("fax")) is unicode:
                print "   new fax number:", addrs[addr]["fax"]
                Phone.objects.create(number=addrs[addr]["fax"], type="fax", address=_addr)
            elif type(addrs[addr].get("fax")) is list:
                for fax in addrs[addr].get("fax"):
                    print "   new fax number:", fax
                    Phone.objects.create(number=fax, type="fax", address=_addr)

    return _mp

def _create_mp_mandates(mandates, _mp):
    c = lambda x: True if x == "true" else False
    d = lambda x: date(int(x["year"]), int(x["month"]), int(x["day"])) if x else None
    if mandates.get("mandate"):
        if type(mandates["mandate"]) is list:
            for mandate in mandates["mandate"]:
                print "   new mandate", mandate["type"]
                if type(mandate.get("end_term")) is list:
                    mandate["end_term"] = mandate["end_term"][0]
                Mandate.objects.create(current=c(mandate["current"]),
                                       mp=_mp,
                                       type=mandate["type"],
                                       role=mandate.get('role'),
                                       institution=mandate.get('institution'),
                                       election_date=d(mandate.get("election_date")),
                                       end_term=d(mandate.get("end_term")),
                                       begin_term=d(mandate.get("begin_term")),
                                       begin_reason=mandate.get("begin_term").get("reason")
                                                  if mandate.get("begin_term") and
                                                  mandate.get("begin_term").get("reason")
                                                  else None,
                                       end_reason=mandate.get("end_term").get("reason")
                                                  if mandate.get("end_term") and
                                                  mandate.get("end_term").get("reason")
                                                  else None)
        else:
            print "   new mandate", mandates["mandate"]["type"]
            Mandate.objects.create(current=c(mandates["mandate"]["current"]),
                                   mp=_mp,
                                   type=mandates["mandate"]["type"],
                                   role=mandates["mandate"].get('role'),
                                   institution=mandates["mandate"].get('institution'),
                                   election_date=d(mandates["mandate"].get("election_date")),
                                   begin_term=d(mandates["mandate"].get("begin_term")),
                                   end_term=d(mandates["mandate"].get("end_term")),
                                   begin_reason=mandates["mandate"].get("begin_term").get("reason")
                                       if mandates["mandate"].get("begin_term") and
                                       mandates["mandate"].get("begin_term").get("reason")
                                       else None,
                                   end_reason=mandates["mandate"].get("end_term").get("reason")
                                       if mandates["mandate"].get("end_term") and
                                       mandates["mandate"].get("end_term").get("reason")
                                       else None)

def manage_mps(path):
    clean_mps()
    print
    print "Load mps json."
    mps = json.loads(open(os.path.join(path, MPS), "r").read())
    print
    a = 0
    for mp in mps:
        a += 1
        print "  *", a, "-", mp["infos"]["name"]["first"], mp["infos"]["name"]["last"], "-", mp["_id"]
        _create_mp_departments(mp)
        _create_mp_groups(mp["infos"]["group"])
        _create_mp_groups(mp["infos"]["group"])
        _create_mp_departments(mp)
        _mp = _create_mp(mp)
        _create_mp_mandates(mp["mandates"], _mp)
        _create_mp_functions(mp, _mp)
        _create_mp_opinions(mp["opinions"], _mp)

def _create_votes(vote):
    _v = Vote.objects.create(id=vote["wiki"], title=vote["label"])
    d = lambda x: datetime(int(x["year"]), int(x["month"]), int(x["day"]), int(x["hour"]), int(x["minute"]), int(x["second"]))

    for v in vote["vote"]:
        print "   new subvote:", v["subject"]["part"]
        SubVote.objects.create(description=v["subject"]["description"], subject=v["subject"]["text"], part=v["subject"]["part"], vote=_v, weight=v["subject"].get("weight"), datetime=d(v["date"]), recommendation=v["subject"].get("recommendation"))
        for r in v["result"]["mep"]:
            if r.get("dbxmlid"):
                print "   create new result:", r["name"], ":", r["choice"], r.get("dbxmlid", "")
                if MEP.objects.filter(key_name=r["dbxmlid"]):
                    Result.objects.create(choice=r["choice"], name=r["name"], mep=MEP.objects.get(key_name=r["dbxmlid"]))

def manage_votes(path):
    clean_votes()
    print
    print "Load votes json."
    votes = json.loads(open(os.path.join(path, VOTES), "r").read())
    print
    a = 0
    for vote in votes:
        a += 1
        print "  *", a, "-", vote["label"]
        _create_votes(vote)

if __name__ == "__main__":
    path = sys.argv[1]
    manage_meps(path)
    manage_mps(path)
    manage_votes(path)
