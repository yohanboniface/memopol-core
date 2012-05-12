from re import sub
from json import load
from reps.models import Opinion, OpinionREP, Representative
from meps.models import MEP
from dateutil.parser import parse

def get_or_create(klass, _id=None, **kwargs):
    if _id is None:
        object = klass.objects.filter(**kwargs)
    else:
        object = klass.objects.filter(**{_id : kwargs[_id]})
    if object:
        return object[0]
    else:
        print "     add new", klass.__name__, kwargs
        return klass.objects.create(**kwargs)

def clean_text(text):
    def rep(result):
        string = result.group()                   # "&#xxx;"
        n = int(string[2:-1])
        uchar = unichr(n)                         # matching unicode char
        return uchar

    return sub("(\r|\t|\n| )+", " ", sub("&#\d+;", rep, text)).strip()

if __name__ == "__main__":
    print "cleaning old opinions"
    Opinion.objects.all().delete()
    OpinionREP.objects.all().delete()
    for op in load(open("opinions.json")):
        op["body"] = "\n".join(op["body"])
        op["body"] = sub("\n\n+", "\n\n", op["body"])
        op["body"] = sub("\n+$", "", op["body"])
        op["body"] = sub("^\n+", "", op["body"])
        op["body"] = op["body"].replace("\n\n", "</p><p>")
        op["body"] = op["body"].replace("\n", "<br>")
        op["body"] = "<p>" + op["body"] + "</p>"
        #print op["body"]
        rep = Representative.objects.get(id=op["mep"])
        if MEP.objects.filter(representative_ptr=rep):
            institution = "EU"
        else:
            institution = "FR"
        #print "http://www.laquadrature.net/wiki/%s" % rep.id
        opinion = get_or_create(Opinion, title=clean_text(op["title"]), content=op["body"], url=op.get("url", ""), institution=institution)
        #print "date:", [op.get("date", "")]
        if "Merci d'enrichir cette partie en y rapportant les prises de positions de " in op["body"]:
            raise Exception

        OpinionREP.objects.create(representative=rep, opinion=opinion, date=parse(op.get("date")).date())
