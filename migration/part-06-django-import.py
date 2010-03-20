#!/usr/bin/python

import sys, os

import couchdb

from memopol2.show.models import Mep, Position

print "Deleting existing django meps"
Mep.objects.all().delete()

#django_meps = Mep.objects.all()
#print "Existing meps in django db:", len(django_meps)
#existing_id_set = set([x.couchid for x in django_meps])
existing_id_set = set()

server = couchdb.Server(os.getenv("COUCH_URL_ROOT"))
meps = server["meps"]

print "Meps in couch db:", len(meps)

for mepid in meps:
    if mepid not in existing_id_set:
        newmep = Mep(couchid=mepid)
        newmep.save()
