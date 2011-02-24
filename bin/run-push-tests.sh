#!/bin/sh
export PYTHONPATH="apps/:"$PYTHONPATH

django-admin.py test --settings=memopol2.testsettings --with-coverage --cover-package=memopol2 --with-xunit --with-xcoverage
django-admin.py  harvest  --settings=memopol2.testsettings  -a memopol2.main