# -*- coding:Utf-8 -*-
import os
import sys
import time
import re
from json import load
from urllib2 import urlopen, HTTPError
from dateutil.parser import parse
from django.db import transaction

from memopol.base.utils import get_or_create

from memopol.reps.models import Email, WebSite
from memopol.mps.models import MP, Department, Circonscription, Group, Function, FunctionMP

if not os.path.exists("dumps"):
    os.mkdir("dumps")


def read_or_dl(url, name, prefix):
    if not os.path.exists(prefix):
        os.makedirs(prefix)
    if not os.path.exists("%s/%s" % (prefix, name)):
        open("%s/%s" % (prefix, name), "w").write(urlopen(url).read())

    return open("%s/%s" % (prefix, name), "r")


def update_personal_informations(_mp, mp):
    _mp.full_name = mp["nom"]
    _mp.last_name = mp["nom_de_famille"]
    _mp.first_name = mp["prenom"]
    _mp.an_webpage = mp["url_an"]
    _mp.profession = mp["profession"]
    _mp.gender = mp["sexe"].replace("H", "M")
    try:
        _mp.birth_date = parse(mp["date_naissance"])
    except:
        print "[Warning] No birth date for " + mp["nom"].encode("Utf-8")

    try:
        _mp.hemicycle_site = mp["place_en_hemicycle"]
    except:
        _mp.hemicycle_site = 0
        _mp.active = False
    if mp["lieu_naissance"] is not None:
        _mp.birth_place = re.sub("\(.*", "", mp["lieu_naissance"])
        _mp.birth_department = re.sub(".*\(", "", mp["lieu_naissance"])[:-1]


def update_group_info(_mp, mp):
    an_id = mp["url_an"].split("/")[-1].split(".")[0]
    if an_id in ("1931", "267553", "267456", "2090", "2769", "632", "2681",
                 "331339", "333224", "267419", "267605", "408269", "1236",
                 "1310", "332", "267165", "346886", "1068", "267285", "345727",
                 "331481", "267872", "267591", "2107", "430"): # mp for which I have data but RC don't
        return
    if an_id in ("267765",):
        _mp.group = get_or_create(Group, abbreviation="NI", name=u"Députés n'appartenant à aucun groupe")
        return
    _mp.group_role = mp["groupe"]["fonction"]
    _mp.group = get_or_create(Group, _id="abbreviation", abbreviation=mp["groupe_sigle"], name=mp["groupe"]["organisme"])


def get_etudes_groups(_mp, mp):
    for i in mp["groupes_parlementaires"]:
        group = i["responsabilite"]
        tipe = " ".join(group["organisme"].split()[:2])
        title = " ".join(group["organisme"].split()[2:])
        if tipe.encode("Utf-8") not in ("Groupe d'amitié", "Groupe d'études"):
            print group["organisme"]
            raise Exception

        function = get_or_create(Function, title=title, type=tipe)
        get_or_create(FunctionMP, mp=_mp, function=function, role=group["fonction"], extra_parliamentary=False)


def get_other_functions(_mp, mp):
    handle_strange_api = lambda x: x if x else []
    for i in handle_strange_api(mp["responsabilites"]):
        handle_function(i, _mp, False)
    for i in handle_strange_api(mp["responsabilites_extra_parlementaires"]):
        handle_function(i, _mp, True)

def handle_function(i, _mp, extra):
    function = i["responsabilite"]
    if function["organisme"].startswith("Bureau"):
        tipe = "bureau"
    elif function["organisme"].encode("Utf-8").startswith("Comité") or function["organisme"].encode("Utf-8").startswith("Comuté"):
        tipe = u"comité"
    elif function["organisme"].startswith("Commission") or function["organisme"].startswith("Commision"):
        tipe = "commission"
    elif function["organisme"].encode("Utf-8").startswith("Délégation"):
        tipe = "déléguation"
    elif function["organisme"].encode("Utf-8").startswith("Observatoire"):
        tipe = "observatoire"
    elif function["organisme"].startswith("Mission") or "- mission" in function["organisme"]:
        tipe = "mission"
    elif function["organisme"].encode("Utf-8").startswith("Office parlementaire"):
        tipe = "office"
    elif function["organisme"].encode("Utf-8").startswith("Groupe de travail"):
        tipe = "groupe de travail"
    elif function["organisme"].encode("Utf-8").startswith("Conseil") or "conseil" in function["organisme"]:
        tipe = "conseil"
    elif function["organisme"].encode("Utf-8").startswith("Groupe français"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("écologie, du développement durable, des transports et du logement"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Modalités de création des brigades de police spécialisées dans la prise en charge des mineurs dél"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Section française de "):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Cour de justice de la république"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Conférence"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Agence nationale"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Haut comité"):
        tipe = "autre"
    elif function["organisme"].encode("Utf-8").startswith("Institut"):
        tipe = "autre"
    else:
        print function["organisme"]
        raise Exception
    new_function = get_or_create(Function, title=function["organisme"], type=tipe)
    get_or_create(FunctionMP, mp=_mp, function=new_function, role=function["fonction"], extra_parliamentary=extra)


def get_department_and_circo(mp, _mp):
    if mp["num_deptmt"] in (999, "999"):
        department = get_or_create(Department, name="Etranger", number="999")
    elif mp["num_deptmt"] != 0:
        try:
            department = Department.objects.get(number=mp["num_deptmt"])
        except:
            if mp["num_deptmt"] == "977":
                department = Department.objects.create(number="977", name=mp["nom_circo"])
            else:
                print "[Error] Department not in database : " + mp["num_deptmt"]
                return
    else: # TOREMOVE: code is fixed on nosdeputes side but cache is still active
        department = Department.objects.get(number=987)
    if mp["num_circo"] != 1:
        number = str(mp["num_circo"]) + "ème"
    else:
        number = str(mp["num_circo"]) + "ère"
    _mp.department = department
    try:
        _mp.circonscription = Circonscription.objects.get(number=number, department=department)
    except:
        _mp.circonscription = get_or_create(Circonscription,
                number=number, department=department)
        print "[Warning] Created new Circonscription : " + number


def get_new_websites(mp, _mp):
    if mp["sites_web"]:
        for website in mp["sites_web"]:
            get_or_create(WebSite, url=website["site"], representative=_mp.representative_ptr)


def get_new_emails(mp, _mp):
    for email in mp["emails"]:
        get_or_create(Email, email=email["email"], representative=_mp.representative_ptr)

def get_mandate(mp, _mp):
    for mandate in mp["mandat_debut"]:
        get_or_create(Mandate, begin_term=mandate["mandat_debut"], representative=_mp.representative_ptr)

def create_uniq_id(mp_json):
    id = mp_json["prenom"].capitalize().replace(" ", "") + mp_json["nom_de_famille"].capitalize().replace(" ", "")
    return re.sub("\W", "", unidecode.unidecode(id))



#Create a new mp that is empty
#we will then fill it with the common update
def create_new_mp(mp):
    _mp = MP()
    _mp.id = create_uniq_id(mp)
    _mp.picture = _mp.id + ".jpg"
    _mp.an_id=mp["url_an"].split("/")[-1].split(".")[0]
    if mp["place_en_hemicycle"] :
        _mp.hemicycle_sit = mp["place_en_hemicycle"]
        _mp.active = True
    else:
        _mp.hemicycle_sit = 0
        _mp.active = False
    update_personal_informations(_mp, mp)
    update_group_info(_mp, mp)
    get_department_and_circo(mp, _mp)
    _mp.save()
    #get_new_emails(mp, _mp)

    #_mp.save()
    print "MP created !"
    return _mp


def update_mps(mps, prefix):
    #update all MP to inactive
    MP.objects.filter(active=True).update(active=False)

    a = 0
    for depute in mps["deputes"]:
        a += 1
        try:
            an_id = depute["depute"]["url_an"].split("/")[-1].split(".")[0]
            print an_id, " : ", depute["depute"]["url_nosdeputes_api"]

            mp = load(read_or_dl(depute["depute"]["url_nosdeputes_api"], an_id, prefix))["depute"]
        except HTTPError:
            try:
                print "Warning, failed to get a deputy, retrying in one seconde (url: %s)" % depute["depute"]["api_url"]
                time.sleep(1)
                mp = load(urlopen(depute["depute"]["url_nosdeputes_api"]))["depute"]
            except HTTPError:
                print "Didn't managed to get this deputy, abort"
                print "Go repport the bug on irc.freenode.net#regardscitoyens"
                sys.exit(1)
        #except :
        #    print "[Error] could not load this MP : " + mp["nom"].encode("Utf-8")
        #    continue
        print a, "-", mp["nom"].encode("Utf-8")
        _mp = MP.objects.filter(an_id=mp["url_an"].split("/")[-1].split(".")[0])
        print _mp
        if not _mp:
            print "missing:", mp["nom"].encode("Utf-8")
            _mp = create_new_mp(mp)
            #_mp = MP.objects.filter(an_id=mp["url_an"].split("/")[-1].split(".")[0])

            if not _mp:
                exit
        else:
            print _mp
            _mp = _mp[0]
        if not depute["depute"].get("ancien_depute"):
            _mp.active = True
        update_personal_informations(_mp, mp)

        # clean
        FunctionMP.objects.filter(mp=_mp).delete()
        update_group_info(_mp, mp)
        get_etudes_groups(_mp, mp)

        get_other_functions(_mp, mp)
        get_new_emails(mp, _mp)
        get_new_websites(mp, _mp)
        get_department_and_circo(mp, _mp)
        _mp.save()

if __name__ == "__main__":
    old_mps = load(read_or_dl("http://2007-2012.nosdeputes.fr/deputes/json", "all_mps", "old_dumps"))
    mps = load(read_or_dl("http://www.nosdeputes.fr/deputes/json", "all_mps", "dumps"))

    with transaction.commit_on_success():
        update_mps(old_mps, "old_dumps")
        update_mps(mps, "dumps")
