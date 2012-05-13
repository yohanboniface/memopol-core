# -*- coding: utf-8 -*-
from os import mkdir
from os.path import exists
from re import search
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from json import dumps
from dateutil.parser import parse

TO_IGNORE = [
    "[date inconnue]",
    u"[Premier trimestre 2010] Européana (librairie numérique)",
    "Internet",
    u"[Date inconnue] Libertés publiques, libertés fondamentales",
    u"[date inconnue probablement fin 2009] Internet, vente de médicaments",
    u"contrefaçon de médicaments",
    "[date inconnue]",
    u"[Premier trimestre 2010] Européana (librairie numérique)",
    u"[date inconnue] Wikileaks, Internet",
    u"Paquet télécom, avant le vote",
]


def read_or_dl(url, name):
    if exists('dumps/%s' % name):
        return BeautifulSoup(open('dumps/%s' % name, 'r').read())
    html = urlopen(url).read()
    open('dumps/%s' % name, 'w').write(html)
    return BeautifulSoup(html)


def handle_reps_set(set_name, section):
    opinions = []
    size = len(open(set_name, "r").read().split('\n'))
    for a, i in enumerate(open(set_name, "r"), 1):
        i = i.replace('\n', '')
        print "[%s/%s]" % (a, size), i
        soup = read_or_dl("http://www.laquadrature.net/wiki/%s?test=true" % i, i)
        if soup.find('div', id='bodyContent').h5 is None:
            continue
        opinion = {}
        if soup.find('div', id='bodyContent').h5.a:
            opinion['url'] = soup.find('div', id='bodyContent').h5.a["href"]
            opinion['title'] = soup.find('div', id='bodyContent').h5.a.text
        else:
            opinion['title'] = soup.find('div', id='bodyContent').h5.text
        opinion['date'] = soup.find('div', id='bodyContent').h5.span.contents[0].strip()
        if " " in opinion["date"]:
            guess_date = search("\d\d/\d\d/\d\d\d\d", opinion["date"])
            if guess_date is not None:
                opinion["date"] = guess_date.group()
            elif opinion["date"] in TO_IGNORE:
                opinion["date"] = None
            else:
                print opinion["date"]
                from ipdb import set_trace; set_trace()
        if opinion["date"] in TO_IGNORE:
            opinion["date"] = None
        elif opinion["date"] == "0504/2011":
            opinion["date"] = "05/04/2011"
        try:
            if opinion["date"] is not None:
                parse(opinion["date"])
        except ValueError:
            print opinion["date"]
            from ipdb import set_trace; set_trace()
        opinion['mep'] = i
        opinion['section'] = section
        opinion['body'] = []
        for x in soup.find('div', id='bodyContent').h5.nextSiblingGenerator():
            if (x.text if hasattr(x, 'text') else x).startswith("Merci d'enrichir cette partie en y rapportant les prises de positions de "):
                continue
            if x.startswith is not None and x.startswith(' \nNewPP limit report'):
                break
            if hasattr(x, "name") and x.name == "h5":
                print dumps(opinion)
                opinions.append(opinion)
                opinion = {}
                if x.a:
                    opinion['title'] = x.a.text
                    opinion['url'] = x.a["href"]
                else:
                    opinion['title'] = x.text
                opinion['mep'] = i
                opinion['section'] = section
                opinion['date'] = x.span.contents[0].strip()
                if " " in opinion["date"]:
                    guess_date = search("\d\d/\d\d/\d\d\d\d", opinion["date"])
                    if guess_date is not None:
                        opinion["date"] = guess_date.group()
                    elif opinion["date"] == "Mai-Juin 2011":
                        opinion["date"] = "25/05/2011"
                    elif opinion["date"] == "04/2010 ACTA":
                        opinion["date"] = "01/04/2010"
                    elif opinion["date"] in ["10/2010 ACTA", "10/2010 ACTA/Hadopi"]:
                        opinion["date"] = "01/10/2010"
                    elif opinion["date"] == "12/2010 Wikileaks":
                        opinion["date"] = "01/12/2010"
                    elif opinion["date"] == u"02/2011 Internet, pédophilie":
                        opinion["date"] = "01/02/2011"
                    elif opinion["date"] in TO_IGNORE:
                        opinion["date"] = None
                    else:
                        print opinion["date"]
                        from ipdb import set_trace; set_trace()
                if opinion["date"] in TO_IGNORE:
                    opinion["date"] = None
                try:
                    if opinion["date"] is not None:
                        parse(opinion["date"])
                except ValueError:
                    print opinion["date"]
                    from ipdb import set_trace; set_trace()
                opinion['body'] = []
            else:
                opinion['body'] += [unicode(x.text if hasattr(x, 'text') else x)]

        print dumps(opinion)
        opinions.append(opinion)

    return opinions

if __name__ == "__main__":
    if not exists('dumps'):
        mkdir("dumps")
    opinions = handle_reps_set("mp_list", "fr")
    opinions += handle_reps_set("mep_list", "eu")

    open('opinions.json', 'w').write(dumps(opinions, indent=4))
