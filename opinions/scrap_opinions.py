# -*- coding: utf-8 -*-
from os import mkdir
from os.path import exists
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from json import dumps

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
        soup = read_or_dl("http://www.laquadrature.net/wiki/index.php?title=%s/fr" % i, i)
        if soup.find('div', id='bodyContent').h5 is None:
            continue
        opinion = {}
        if soup.find('div', id='bodyContent').h5.a:
            opinion['url'] = soup.find('div', id='bodyContent').h5.a["href"]
            opinion['title'] = soup.find('div', id='bodyContent').h5.a.text
        else:
            opinion['title'] = soup.find('div', id='bodyContent').h5.text
        opinion['date'] = soup.find('div', id='bodyContent').h5.span.contents[0].strip()
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
