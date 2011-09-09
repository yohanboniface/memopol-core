import sys
from json import load
from urllib2 import urlopen

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
            _mp.save()
