# encoding: utf-8

import os
import json
import re
import unidecode
from os.path import join
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db import transaction
from django.conf import settings

from meps.utils import update_meps_positions
from memopol2.utils import update_search_index, get_or_create

from reps.models import PartyRepresentative, Email, WebSite, CV
from meps.models import LocalParty, MEP, Delegation, DelegationRole, PostalAddress, Country, CountryMEP, Organization, OrganizationMEP, Committee, CommitteeRole, Group, GroupMEP, Building


JSON_DUMP_ARCHIVE_LOCALIZATION = join(settings.MEMOPOL_TMP_DIR, "ep_meps_current.json.xz")
JSON_DUMP_LOCALIZATION = join(settings.MEMOPOL_TMP_DIR, "ep_meps_current.json")
_parse_date = lambda date: datetime.strptime(date, "%Y-%m-%dT00:%H:00")


class Command(BaseCommand):
    help = 'Update the eurodeputies data by pulling it from parltrack'

    def handle(self, *args, **options):
        print "clean old downloaded files"
        os.system("rm %s %s" % (JSON_DUMP_ARCHIVE_LOCALIZATION, JSON_DUMP_LOCALIZATION))
        print "download lastest data dump of meps from parltrack"
        os.system("wget http://parltrack.euwiki.org/dumps/ep_meps_current.json.xz -O %s" % JSON_DUMP_ARCHIVE_LOCALIZATION)
        print "unxz dump"
        os.system("unxz %s" % JSON_DUMP_ARCHIVE_LOCALIZATION)
        print "load json"
        meps = json.load(open(JSON_DUMP_LOCALIZATION, "r"))
        print "Set all current active mep to unactive before importing"
        with transaction.commit_on_success():
            MEP.objects.filter(active=True).update(active=False)
            a = 0
            for mep_json in meps:
                a += 1
                print a, "-", mep_json["Name"]["full"].encode("Utf-8")
                in_db_mep = MEP.objects.filter(ep_id=int(mep_json["UserID"]))
                if in_db_mep:
                    mep = in_db_mep[0]
                    mep.active = mep_json['active']
                    manage_mep(mep, mep_json)
                else:
                    mep = create_mep(mep_json)
            clean()
        print
        update_meps_positions(verbose=True)
        update_search_index()


def create_uniq_id(mep_json):
    id = mep_json["Name"]["sur"].capitalize().replace(" ", "") + mep_json["Name"]["family"].capitalize().replace(" ", "")
    return re.sub("\W", "", unidecode.unidecode(id))

def add_committees(mep, committees):
    CommitteeRole.objects.filter(mep=mep).delete()
    for committee in committees:
        if committee.get("committee_id"):
            try:
                    in_db_committe = Committee.objects.get(abbreviation=committee["committee_id"])
            except Committee.DoesNotExist:
                print "     create new commitee:", committee["committee_id"], committee["Organization"]
                in_db_committe = Committee.objects.create(name=committee["Organization"],
                                                          abbreviation=committee["committee_id"])
            print "     link mep to commmitte:", committee["Organization"]
            params={}
            if committee.get("start"):
                params['begin']=_parse_date(committee.get("start"))
            if committee.get("end"):
                params['end']=_parse_date(committee.get("end"))
            CommitteeRole.objects.create(mep=mep, committee=in_db_committe,
                                         role=committee["role"], **params)
                                         #begin=_parse_date(committee.get("start")),
                                         #end=_parse_date(committee.get("end")))
        else:
            # FIXME create or how abbreviations ? Or are they really important ? or create a new class ?
            print "WARNING: committe without abbreviation:", committee["Organization"]

def add_delegations(mep, delegations):
    DelegationRole.objects.filter(mep=mep).delete()
    for delegation in delegations:
        db_delegation = get_or_create(Delegation, name=delegation["Organization"])
        print "     create DelegationRole to link mep to delegation"
        params={}
        if delegation.get("start"):
            params['begin']=_parse_date(delegation["start"])
        if delegation.get("end"):
            params['end']=_parse_date(delegation["end"])
        DelegationRole.objects.create(mep=mep, delegation=db_delegation,
                                      role=delegation["role"], **params)
                                      #begin=_parse_date(delegation["start"]),
                                      #end=_parse_date(delegation["end"]))

def add_addrs(mep, addrs):
    if addrs.get("Brussels"):
        print "     add Brussels infos"
        bxl = addrs["Brussels"]
        if bxl["Address"].get("building_code"):
            mep.bxl_building = get_or_create(Building, _id="id",
                                         id=bxl["Address"]["building_code"],
                                         name=bxl["Address"]["Building"],
                                         street=bxl["Address"]["Street"],
                                         postcode=bxl["Address"]["Zip"])
        mep.bxl_floor = bxl["Address"]["Office"][:2]
        mep.bxl_office_number = bxl["Address"]["Office"][2:]
        mep.bxl_fax = bxl["Fax"]
        mep.bxl_phone1 = bxl["Phone"]
        mep.bxl_phone2 = bxl["Phone"][:-4] + "7" + bxl["Phone"][-3:]
    print "     add Strasbourg infos"
    if addrs.get("Strasbourg"):
        stg = addrs["Strasbourg"]
        if stg["Address"].get("building_code"):
            mep.stg_building = get_or_create(Building, _id="id",
                                         id=stg["Address"]["building_code"],
                                         name=stg["Address"]["Building"],
                                         street=stg["Address"]["Street"],
                                         postcode=stg["Address"].get("Zip", stg["Address"]["Zip1"]))
        mep.stg_floor = stg["Address"]["Office"][:3]
        mep.stg_office_number = stg["Address"]["Office"][3:]
        mep.stg_fax = stg["Fax"]
        mep.stg_phone1 = stg["Phone"]
        mep.stg_phone2 = stg["Phone"][:-4] + "7" + stg["Phone"][-3:]
        print "     adding mep's postal addresses:"
    mep.save()
    PostalAddress.objects.filter(mep=mep).delete()
    for addr in addrs.get("Postal", []):
        print "       *", addr.encode("Utf-8")
        PostalAddress.objects.create(addr=addr, mep=mep)

def add_countries(mep, countries):
    PartyRepresentative.objects.filter(representative=mep.representative_ptr).delete()
    CountryMEP.objects.filter(mep=mep).delete()
    print "     add countries"
    for country in countries:
        print country
        print "     link mep to country", '"%s"' % country["country"], "for a madate"
        _country = Country.objects.get(name=country["country"])
        print "     link representative to party"
        if "party" in country:
            party = get_or_create(LocalParty, name=country["party"], country=_country)
            if not PartyRepresentative.objects.filter(representative=mep.representative_ptr, party=party):
                #current = True if _parse_date(country["end"]).year > date.today().year else False
                current = 'end' not in country
                PartyRepresentative.objects.create(representative=mep.representative_ptr,
                                                   party=party, current=current)
        else: party=get_or_create(LocalParty, name="unknown", country=_country)
        params={}
        if country.get("start"):
            params['begin']=_parse_date(country["start"])
        if country.get("end"):
            params['end']=_parse_date(country["end"])
        CountryMEP.objects.create(mep=mep, country=_country, party=party, **params)
                                  #begin=_parse_date(country["start"]),
                                  #end=_parse_date(country["end"]))

def add_organizations(mep, organizations):
    OrganizationMEP.objects.filter(mep=mep).delete()
    for organization in organizations:
        in_db_organization = get_or_create(Organization, name=organization["Organization"])
        print "     link mep to organization:", in_db_organization.name
        params={}
        if organization.get("start"):
            params['begin']=_parse_date(organization["start"])
        if organization.get("end"):
            params['end']=_parse_date(organization["end"])
        OrganizationMEP.objects.create(mep=mep,
                                       organization=in_db_organization,
                                       role=organization["role"], **params)
                                       #begin=_parse_date(organization["start"]),
                                       #end=_parse_date(organization["end"]))

def change_mep_details(mep, mep_json):
    if mep_json.get("Birth"):
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
    print "     update mep gender"
    if mep_json["Gender"] == u'n/a':
        mep.gender = None
    else:
        mep.gender = mep_json["Gender"]

def add_mep_email(mep, emails):
    if isinstance(emails, list):
        for email in emails:
            get_or_create(Email, representative=mep.representative_ptr, email=email)
    else:
        get_or_create(Email, representative=mep.representative_ptr, email=emails)

def add_mep_website(mep, urls):
    for url in urls:
        get_or_create(WebSite, representative=mep.representative_ptr, url=url)

def add_mep_cv(mep, cv):
    for c in cv:
        if c:
            get_or_create(CV, title=c, representative=mep.representative_ptr)

def add_groups(mep, groups):
    # I don't create group if they don't exist for the moment
    convert = {"S&D": "SD", "NA": "NI", "ID": "IND/DEM", "PPE": "EPP", "Verts/ALE": "Greens/EFA"}
    GroupMEP.objects.filter(mep=mep).delete()
    for group in groups:
        if not group.get("groupid"):
            continue
        print "     link mep to group", group["groupid"], group["Organization"]
        if type(group["groupid"]) is list:
            # I really don't like that hack
            group["groupid"] = group["groupid"][0]
        group["groupid"] = convert.get(group["groupid"], group["groupid"])
        in_db_group = Group.objects.filter(abbreviation=group["groupid"])
        if in_db_group:
            in_db_group = in_db_group[0]
        else:
            in_db_group = Group.objects.create(abbreviation=group["groupid"], name=group["Organization"])
        params={}
        if group.get("start"):
            params['begin']=_parse_date(group["start"])
        if group.get("end"):
            params['end']=_parse_date(group["end"])
        GroupMEP.objects.create(mep=mep, group=in_db_group, role=group["role"])
                                #begin=_parse_date(group["start"]),
                                #end=_parse_date(group["end"]))

def manage_mep(mep, mep_json):
    change_mep_details(mep, mep_json)
    mep.committeerole_set.all().delete()
    add_committees(mep, mep_json.get("Committees", []))
    add_delegations(mep, mep_json.get("Delegations", []))
    add_countries(mep, mep_json["Constituencies"])
    add_groups(mep, mep_json.get("Groups", []))
    if mep_json.get("Addresses"):
        add_addrs(mep, mep_json["Addresses"])
    add_organizations(mep, mep_json.get("Staff", []))
    if mep_json.get("Mail"):
        add_mep_email(mep, mep_json["Mail"])
    mep.website_set.filter(url="").delete()
    if mep_json.get("Homepage"):
        add_mep_website(mep, mep_json["Homepage"] + mep_json.get("Twitter", []) + mep_json.get("Facebook", []))
    add_mep_cv(mep, mep_json.get("CV", []))
    print "     save mep modifications"
    mep.save()

def add_missing_details(mep, mep_json):
    mep.ep_id = int(mep_json["UserID"])

def create_mep(mep_json):
    mep = MEP()
    mep.id = create_uniq_id(mep_json)
    mep.picture = mep.id + ".jpg"
    mep.active = True
    change_mep_details(mep, mep_json)
    add_missing_details(mep, mep_json)
    if mep_json.get("Addresses"):
        add_addrs(mep, mep_json["Addresses"])
    mep.save()
    add_committees(mep, mep_json.get("Committees", []))
    add_delegations(mep, mep_json.get("Delegations", []))
    add_countries(mep, mep_json["Constituencies"])
    add_groups(mep, mep_json["Groups"])
    add_organizations(mep, mep_json.get("Staff", []))
    if mep_json.get("Mail"):
        add_mep_email(mep, mep_json["Mail"])

    if mep_json.get("Homepage"):
        add_mep_website(mep, mep_json["Homepage"] + mep_json.get("Twitter", []) + mep_json.get("Facebook", []))
    add_mep_cv(mep, mep_json.get("CV", []))
    print "     save mep modifications"
    mep.save()

def clean():
    Delegation.objects.annotate(mep_count=Count('mep')).filter(mep_count=0).delete()
    Committee.objects.annotate(mep_count=Count('mep')).filter(mep_count=0).delete()
    Organization.objects.annotate(mep_count=Count('mep')).filter(mep_count=0).delete()

# vim:set shiftwidth=4 tabstop=4 expandtab:
