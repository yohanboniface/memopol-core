#!/bin/sh
django-admin.py test --settings=memopol2.testsettings --with-coverage --cover-package=memopol2 --with-xunit --with-xcoverage
