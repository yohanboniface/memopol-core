#!/usr/bin/python

import sys
import httplib
import os

import anyjson



input_name = sys.argv[1]
db_name = "/" + sys.argv[2] + "/"

jsondata = anyjson.deserialize(open(input_name, "r").read())
for item in jsondata:
    server = httplib.HTTPConnection(os.getenv("COUCH_HOST"), int(os.getenv("COUCH_PORT")))
    server.request("POST", db_name, anyjson.serialize(item))
    r = server.getresponse()
    r.read()
    print r.status
