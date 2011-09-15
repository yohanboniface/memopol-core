import sys
from json import load
from urllib2 import urlopen

from memopol2.utils import get_or_create

from reps.models import Email, WebSite
from mps.models import MP

if __name__ == "__main__":
    mps = load(urlopen("http://www.nosdeputes.fr/deputes/json"))

    print "Setting all mps to unactive"
    a = 0
    total = MP.objects.count()
    for mp in MP.objects.all():
        a += 1
        mp.active = False
        mp.save()
        sys.stdout.write("%i/%i\r" % (a, total))
        sys.stdout.flush()
    sys.stdout.write("\n")

    a = 0
    for depute in mps["deputes"]:
        a += 1
        mp = load(urlopen(depute["depute"]["api_url"]))["depute"]
        print a, "-", mp["nom"]
        _mp = MP.objects.filter(an_id=mp["url_an"].split("/")[-1].split(".")[0])
        if _mp:
            _mp = _mp[0]
            if not depute["depute"].get("ancien_depute"):
                _mp.active = True
            _mp.full_name = mp["nom"]
            _mp.last_name = mp["nom_de_famille"]
            _mp.an_webpage = mp["url_an"]
            _mp.profession = mp["profession"]
            for email in mp["emails"]:
                get_or_create(Email, email=email["email"], representative=_mp.representative_ptr)
            if mp["site_web"]:
                get_or_create(WebSite, url=mp["site_web"], representative=_mp.representative_ptr)
            _mp.save()
