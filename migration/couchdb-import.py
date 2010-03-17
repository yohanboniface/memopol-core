#!/usr/bin/python

import sys
import httplib
import os

from jsonwrapper import json

input_name = sys.argv[1]
db_name = "/" + sys.argv[2] + "/"

jsondata = json.loads(open(input_name, "r").read())
for item in jsondata:
    server = httplib.HTTPConnection(os.getenv("COUCH_HOST"), int(os.getenv("COUCH_PORT")))
    server.request("POST", db_name, json.dumps(item))
    r = server.getresponse()
    r.read()
    print r.status
