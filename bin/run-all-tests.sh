#!/bin/sh
export PYTHONPATH="apps/:"$PYTHONPATH

django-admin.py test --settings=memopol2.testsettings --with-coverage --cover-package=memopol2 --with-xunit --with-xcoverage
django-admin.py harvest  --settings=memopol2.testsettings --verbosity=3 -a memopol2.main
pylint --rcfile=.pylintrc memopol2 | tee pylint.out
