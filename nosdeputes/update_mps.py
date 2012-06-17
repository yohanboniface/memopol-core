import os
import sys
import time
from json import load
from urllib2 import urlopen, HTTPError
from django.db import transaction

from memopol2.utils import get_or_create

from reps.models import Email, WebSite
from mps.models import MP

if not os.path.exists("dumps"):
    os.mkdir("dumps")


def read_or_dl(url, name):
    if not os.path.exists("dumps/%s" % name):
        open("dumps/%s" % name, "w").write(urlopen(url).read())

    return open("dumps/%s" % name, "r")


def update_personal_informations(_mp, mp):
    _mp.full_name = mp["nom"]
    _mp.last_name = mp["nom_de_famille"]
    _mp.first_name = mp["prenom"]
    _mp.an_webpage = mp["url_an"]
    _mp.profession = mp["profession"]


def get_new_websites(mp, _mp):
    if mp["sites_web"]:
        for website in mp["sites_web"]:
            get_or_create(WebSite, url=website["site"], representative=_mp.representative_ptr)


def get_new_emails(mp, _mp):
    for email in mp["emails"]:
        get_or_create(Email, email=email["email"], representative=_mp.representative_ptr)


if __name__ == "__main__":
    mps = load(read_or_dl("http://www.nosdeputes.fr/deputes/json", "all_mps"))

    with transaction.commit_on_success():
        MP.objects.filter(active=True).update(active=False)

        a = 0
        for depute in mps["deputes"]:
            a += 1
            try:
                an_id = depute["depute"]["url_an"].split("/")[-1].split(".")[0]
                mp = load(read_or_dl(depute["depute"]["url_nosdeputes_api"], an_id))["depute"]
            except HTTPError:
                try:
                    print "Warning, failed to get a deputy, retrying in one seconde (url: %s)" % depute["depute"]["api_url"]
                    time.sleep(1)
                    mp = load(urlopen(depute["depute"]["url_nosdeputes_api"]))["depute"]
                except HTTPError:
                    print "Didn't managed to get this deputy, abort"
                    print "Go repport the bug on irc.freenode.net#regardscitoyens"
                    sys.exit(1)
            print a, "-", mp["nom"].encode("Utf-8")
            _mp = MP.objects.filter(an_id=mp["url_an"].split("/")[-1].split(".")[0])
            if _mp:
                _mp = _mp[0]
                if not depute["depute"].get("ancien_depute"):
                    _mp.active = True
                update_personal_informations(_mp, mp)
                get_new_emails(mp, _mp)
                get_new_websites(mp, _mp)
                _mp.save()
