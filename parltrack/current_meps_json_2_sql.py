#!/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import sys
import json
from datetime import datetime, date
from django.db.models import Count

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("parltrack")] + "apps/"]

from reps.models import Party, PartyRepresentative, Email, WebSite, CV
from meps.models import MEP, Delegation, DelegationRole, PostalAddress, Country, CountryMEP, Organization, OrganizationMEP, Committee, CommitteeRole, Group, GroupMEP, Building

current_meps = "meps.json"

_parse_date = lambda date: datetime.strptime(date, "%Y-%m-%dT00:00:00")

def get_or_create(klass, **kwargs):
    object = klass.objects.filter(**kwargs)
    if object:
        return object[0]
    else:
        print "     add new", klass.__name__, kwargs
        return klass.objects.create(**kwargs)

def clean_existant_data(mep):
    print "     remove links with delegations"
    mep.delegationrole_set.all().delete()
    print "     remove links with committees"
    mep.committeerole_set.all().delete()
    print "     remove old postal addrs"
    mep.postaladdress_set.all().delete()

def create_mep(mep_json):
    pass

def add_committees(mep, committees):
    mep.committeerole_set.all().delete()
    for committee in committees:
        if committee.get("committee_id"):
            try:
                    in_db_committe = Committee.objects.get(abbreviation=committee["committee_id"])
            except Committee.DoesNotExist:
                print "     create new commitee:", committee["committee_id"], committee["Organization"]
                in_db_committe = Committee.objects.create(name=committee["Organization"],
                                                          abbreviation=committee["committee_id"])
            print "     link mep to commmitte:", committee["Organization"]
            CommitteeRole.objects.create(mep=mep, committee=in_db_committe,
                                         role=committee["role"],
                                         begin=_parse_date(committee["start"]),
                                         end=_parse_date(committee["end"]))
        else:
            # TODO fix this in parltrack
            print "WARNING: committe without abbreviation:", committee["Organization"]

def add_delegations(mep, delegations):
    for delegation in delegations:
        db_delegation = get_or_create(Delegation, name=delegation["Organization"])
        print "     create DelegationRole to link mep to delegation"
        DelegationRole.objects.create(mep=mep, delegation=db_delegation,
                                      role=delegation["role"],
                                      begin=_parse_date(delegation["start"]),
                                      end=_parse_date(delegation["end"]))

def add_addrs(mep, addrs):
    print "     add Brussels infos"
    bxl = addrs["Brussels"]
    mep.bxl_building = Building.objects.get(id=bxl["Address"]["building_code"])
    mep.bxl_office = bxl["Address"]["Office"]
    mep.bxl_fax = bxl["Fax"]
    mep.bxl_phone1 = bxl["Phone"]
    mep.bxl_phone2 = bxl["Phone"][:-4] + "7" + bxl["Phone"][-3:]
    print "     add Strasbourg infos"
    stg = addrs["Strasbourg"]
    mep.stg_building = Building.objects.get(id=stg["Address"]["building_code"])
    mep.stg_office = stg["Address"]["Office"]
    mep.stg_fax = stg["Fax"]
    mep.stg_phone1 = stg["Phone"]
    mep.stg_phone2 = stg["Phone"][:-4] + "7" + stg["Phone"][-3:]
    print "     adding mep's postal addresses:"
    for addr in addrs["Postal"]:
        print "       *", addr
        PostalAddress.objects.create(addr=addr, mep=mep)

def add_countries(mep, countries):
    print "     add countries"
    for country in countries:
        party = get_or_create(Party, name=country["party"])
        print "     link representative to party"
        if not PartyRepresentative.objects.filter(representative=mep.representative_ptr, party=party):
            current = True if _parse_date(country["end"]).year > date.today().year else False
            PartyRepresentative.objects.create(representative=mep.representative_ptr,
                                               party=party, current=current)
        _country = Country.objects.get(name=country["country"])
        print "     link mep to country", '"%s"' % country["country"], "for a madate"
        CountryMEP.objects.create(mep=mep, country=_country, party=party,
                                  begin=_parse_date(country["start"]),
                                  end=_parse_date(country["end"]))

def add_organizations(mep, organizations):
    for organization in organizations:
        in_db_organization = get_or_create(Organization, name=organization["Organization"])
        print "     link mep to organization:", in_db_organization.name
        OrganizationMEP.objects.create(mep=mep,
                                       organization=in_db_organization,
                                       role=organization["role"],
                                       begin=_parse_date(organization["start"]),
                                       end=_parse_date(organization["end"]))

def change_mep_details(mep, mep_json):
    print "     update mep birth date"
    mep.birth_date = _parse_date(mep_json["Birth"]["date"])
    print "     update mep birth place"
    mep.birth_place = mep_json["Birth"]["place"]
    print "     update mep first name"
    mep.first_name = mep_json["Name"]["sur"]
    print "     update mep last name"
    mep.last_name = mep_json["Name"]["family"]
    print "     update mep full name"
    mep.full_name = "%s %s" %(mep_json["Name"]["sur"], mep_json["Name"]["family"])

def add_mep_email(mep, email):
    get_or_create(Email, representative=mep.representative_ptr, email=email)

def add_mep_website(mep, url):
    get_or_create(WebSite, representative=mep.representative_ptr, url=url)

def add_mep_cv(mep, cv):
    for c in cv:
        if c:
            get_or_create(CV, title=c, representative=mep.representative_ptr)

def add_groups(mep, groups):
    # I don't create group if they don't exist for the moment
    convert = {"S&D": "SD", "NA": "NI" }
    GroupMEP.objects.filter(mep=mep).delete()
    for group in groups:
        print "     link mep to group", group["groupid"], group["Organization"]
        group["groupid"] = convert.get(group["groupid"], group["groupid"])
        in_db_group = Group.objects.get(abbreviation=group["groupid"])
        GroupMEP.objects.create(mep=mep, group=in_db_group, role=group["role"],
                                begin=_parse_date(group["start"]),
                                end=_parse_date(group["end"]))

def manage_mep(mep, mep_json):
    mep.active = True
    change_mep_details(mep, mep_json)
    add_committees(mep, mep_json["Committees"])
    add_delegations(mep, mep_json.get("Delegations", []))
    add_countries(mep, mep_json["Constituencies"])
    add_groups(mep, mep_json["Groups"])
    add_addrs(mep, mep_json["Addresses"])
    add_organizations(mep, mep_json.get("Staff", []))
    add_mep_email(mep, mep_json["Mail"])
    add_mep_website(mep, mep_json["Homepage"])
    add_mep_cv(mep, mep_json.get("CV", []))
    print "     save mep modifications"
    mep.save()

def clean_old_stuff():
    print
    print "* remove empty delegations"
    Delegation.objects.annotate(meps=Count('mep')).filter(meps=0)
    print "* remove empty committees"
    Committee.objects.annotate(meps=Count('mep')).filter(meps=0)
    print "* remove empty organizations"
    Organization.objects.annotate(meps=Count('mep')).filter(meps=0)

if __name__ == "__main__":
    print "load json"
    meps = json.load(open(current_meps, "r"))
    a = 0
    count = meps["count"]
    print "Set all current active mep to unactive before importing"
    for mep in MEP.objects.filter(active=True):
        a += 1
        mep.current = False
        mep.save()
        sys.stdout.write("%3i/%i\r" % (a, count))
    sys.stdout.write("%i/%i" % (a, count))
    a = 0
    for mep_json in meps["meps"]:
        a += 1
        print a, "-", mep_json["Name"]["full"]
        in_db_mep = MEP.objects.filter(ep_id=mep_json["UserID"])
        if in_db_mep:
            mep = in_db_mep[0]
            clean_existant_data(mep)
            manage_mep(mep, mep_json)
        else:
            mep = create_mep(mep_json)
    clean_old_stuff()

# TODO
# need to check all the existant building and to remove the empty one

# vim:set shiftwidth=4 tabstop=4 expandtab:
