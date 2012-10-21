import urllib2, time, cookielib
# -*- coding:utf-8 -*-

opener=None
def init_opener():
    global opener
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
                                  urllib2.ProxyHandler({'http': 'http://localhost:8123/'}))
    opener.addheaders = [('User-agent', 'memopol2')]

def fetch(url, retries=5, ignore=[], params=None):
    if not opener:
        init_opener()
    try:
        f=opener.open(url, params)
    except (urllib2.HTTPError, urllib2.URLError), e:
        if hasattr(e, 'code') and e.code>=400 and e.code not in [504, 502]+ignore:
            logger.warn("[!] %d %s" % (e.code, url))
            raise
        if retries>0:
            time.sleep(4*(6-retries))
            f=fetch(url, retries-1, ignore=ignore, params=params)
        else:
            raise
    return f

committee_map={u'Foreign Affairs': u'AFET',
               u"Regional Policy, Transport and Tourism": u'RETT',
               u'Foreign Affairs': u'AFET',
               u'Human Rights': u'DROI',
               u'Security and Defence': u'SEDE',
               u'Development': u'DEVE',
               u'International Trade': u'INTA',
               u'Budgets': u'BUDG',
               u'Budgetary Control': u'CONT',
               u'Organised crime, corruption and money laundering' : u'CRIM',
               u'Economic and Monetary Affairs': u'ECON',
               u'Employment and Social Affairs': u'EMPL',
               u'Environment, Public Health and Food Safety': u'ENVI',
               u'Industry, Research and Energy': u'ITRE',
               u'Internal Market and Consumer Protection': u'IMCO',
               u'Transport and Tourism': u'TRAN',
               u'Regional Development': u'REGI',
               u'Agriculture and Rural Development': u'AGRI',
               u'Fisheries': u'PECH',
               u'Culture and Education': u'CULT',
               u'Legal Affairs': u'JURI',
               u'Civil Liberties, Justice and Home Affairs': u'LIBE',
               u'Constitutional Affairs': u'AFCO',
               u"Women's Rights and Gender Equality": u'FEMM',
               u"Committee on Women's Rights and Gender": u'FEMM',
               u"Women’s Rights and Gender Equality": u'FEMM',
               u'Petitions': u'PETI',
               u'Financial, Economic and Social Crisis': u'CRIS',
               u'Policy Challenges Committee': u'SURE',
               u'Committee on Foreign Affairs': u'AFET',
               u'Committee on Human Rights': u'DROI',
               u'Committee on Security and Defence': u'SEDE',
               u'Committee on Development': u'DEVE',
               u'Committee on development': u'DEVE',
               u'Special Committee on the Financial, Economic and Social Crisis': u'CRIS',
               u'Special committee on the policy challenges and budgetary resources for a sustainable': u'SURE',
               u'Special committee on the policy challenges and budgetary resources for a sustainable European Union after 2013': u'SURE',
               u'Committee on International Trade': u'INTA',
               u'Committee on Budgets': u'BUDG',
               u'Committee on Budgetary Control': u'CONT',
               u'Committee on Economic and Monetary Affairs': u'ECON',
               u'Committee on Employment and Social Affairs': u'EMPL',
               u"Commission de l'emploi et des affaires sociales": u'EMPL',
               u'Commission des libertés civiles, de la justice et des affaires intérieures': u'LIBE',
               u'Committee on Environment, Public Health and Food Safety': u'ENVI',
               u'Committee on the Environment, Public Health and Food Safety': u'ENVI',
               u'Committee on Industry, Research and Energy': u'ITRE',
               u'Committee on Internal Market and Consumer Protection': u'IMCO',
               u'Committee on the Internal Market and Consumer Protection': u'IMCO',
               u'Committee on Transport and Tourism': u'TRAN',
               u'Committee on Regional Development': u'REGI',
               u'Committee on Agriculture and Rural Development': u'AGRI',
               u'Committee on Agricultural and Rural Development': u'AGRI',
               u'Committee on Committee on Agriculture and Rural Development': u'AGRI',
               u"Commission de l'agriculture et du développement rural": u'AGRI',
               u"Commission du marché intérieur et de la protection des consommateurs": u'IMCO',
               u'Co-Committee on the Internal Market and Consumer Protection': u'IMCO',
               u'COMMITTEE ON THE INTERNAL MARKET AND CONSUMER PROTECTION': u'IMCO',
               u'Committee on Fisheries': u'PECH',
               u'Committee on Culture and Education': u'CULT',
               u'Committee on Legal Affairs': u'JURI',
               u'Committee on Civil Liberties, Justice and Home Affairs': u'LIBE',
               u'Committee on Constitutional Affairs': u'AFCO',
               u"Committee on Women's Rights and Gender Equality": u'FEMM',
               u"Committee on Women’s Rights and Gender Equality": u'FEMM',
               u'Committee on Petitions': u'PETI',
               u'Committee on Financial, Economic and Social Crisis': u'CRIS',
               u'Committee on Policy Challenges Committee': u'SURE'}
