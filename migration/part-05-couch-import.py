#!/usr/bin/env python

import sys
import httplib
import os

import anyjson



input_name = sys.argv[1]
db_name = "/" + sys.argv[2] + "/"

jsondata = anyjson.deserialize(open(input_name, "r").read())
for item in jsondata:
    server = httplib.HTTPConnection(os.getenv("COUCH_HOST"), int(os.getenv("COUCH_PORT")))
    server.request("POST", db_name, anyjson.serialize(item), {"Content-Type": "application/json"})
    r = server.getresponse()
    r.read()
    if r.status < 200 or r.status > 299:
        print "Got a bad http status: %d for item %s in input %s" % (r.status, repr(item), input_name)
