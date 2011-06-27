#!/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import sys
import json
from datetime import datetime

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("parltrack")] + "apps/"]

from reps.models import Party, PartyRepresentative
from meps.models import MEP, Delegation, DelegationRole, PostalAddress, Country, CountryMEP

current_meps = "meps.json"

_parse_date = lambda date: datetime.strptime(date, "%Y-%m-%dT00:00:00")

def clean_existant_data(mep):
    print "   remove links with delegations"
    mep.delegationrole_set.all().delete()
    print "   remove links with committees"
    mep.committeerole_set.all().delete()
    print "   remove old postal addrs"
    mep.postaladdress_set.all().delete()

def create_mep(mep_json):
    pass

def add_committees(mep, committees):
    for committee in committees:
        # TODO
        pass

def add_delegations(mep, delegations):
    for delegation in delegations:
        db_delegation = Delegation.objects.filter(name=delegation["Organization"])
        if db_delegation:
            db_delegation = db_delegation[0]
        else:
            print "   add delegation:", delegation["Organization"]
            db_delegation = Delegation.objects.create(name=delegation["Organization"])
        print "   create DelegationRole to link mep to delegation"
        DelegationRole.objects.create(mep=mep, delegation=db_delegation, role=delegation["role"], begin=_parse_date(delegation["start"]), end=_parse_date(delegation["end"]))

def add_addrs(mep, addrs):
    print "   add Brussels infos"
    bxl = addrs["Brussels"]
    # TODO mep.bxl_building && mep.stg_building
    mep.bxl_office = bxl["Address"]["Office"]
    mep.bxl_fax = bxl["Fax"]
    mep.bxl_phone1 = bxl["Phone"]
    mep.bxl_phone2 = bxl["Phone"][:-4] + "7" + bxl["Phone"][-3:]
    print "   add Strasbourg infos"
    stg = addrs["Strasbourg"]
    mep.stg_office = stg["Address"]["Office"]
    mep.stg_fax = stg["Fax"]
    mep.stg_phone1 = stg["Phone"]
    mep.stg_phone2 = stg["Phone"][:-4] + "7" + stg["Phone"][-3:]
    print "   adding mep's postal addresses:"
    for addr in addrs["Postal"]:
        print "     *", addr
        PostalAddress.objects.create(addr=addr, mep=mep)

def add_countries(mep, countries):
    print "   add countries"
    for country in countries:
        party = Party.objects.filter(name=country["party"])
        if party:
            party = party[0]
        else:
            print "   add missing party"
            party = Party.objects.create(name=country["party"])
            current = False
            # TODO set current according to the current date
            print "   link representative to party"
            # TODO check if not already linked
            PartyRepresentative.objects.create(representative=mep.representative_ptr, party=party, current=current)
        _country = Country.objects.get(name=country["country"])
        print "   link mep to country", '"%s"' % country["country"], "for a madate"
        CountryMEP.objects.create(mep=mep, country=_country, party=party, begin=_parse_date(country["start"]), end=_parse_date(country["end"]))

def manage_mep(mep, mep_json):
    mep.active = True
    add_committees(mep, mep_json["Committees"])
    add_delegations(mep, mep_json["Delegations"])
    add_countries(mep, mep_json["Constituencies"])
    add_addrs(mep, mep_json["Addresses"])
    print "   save mep modifications"
    mep.save()

if __name__ == "__main__":
    print "load json"
    #meps = json.load(open(current_meps, "r"))
    #new = 0
    #to_update = 0
    #for mep_json in meps["meps"]:
    mep_json = json.load(open("one_mep.json", "r"))
    in_db_mep = MEP.objects.filter(ep_id=mep_json["UserID"])
    if in_db_mep:
        mep = in_db_mep[0]
        clean_existant_data(mep)
    else:
        mep = create_mep(mep_json)
    manage_mep(mep, mep_json)
    #print "%i new meps, %i meps to update" % (new, to_update)

# TODO
# need to check all the existant building and to remove the empty one
# same for delegations and committees
# need to set all current mep to current = False before the importation
# also check in reps for emails and stuff like that to remove
# meps urls

# vim:set shiftwidth=4 tabstop=4 expandtab:
