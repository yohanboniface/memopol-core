#!/usr/bin/python
# -*- coding:Utf-8 -*-

import json

current_meps = "meps.json"

if __name__ == "__main__":
    meps = json.load(open(current_meps, "r"))
    for mep in meps["meps"]:
        print mep["Name"]["full"]

# vim:set shiftwidth=4 tabstop=4 expandtab:
