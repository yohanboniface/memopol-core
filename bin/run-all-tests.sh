#!/bin/sh
export PYTHONPATH="apps/:"$PYTHONPATH

django-admin.py test --settings=memopol2.testsettings --with-coverage --cover-package=meps,mps,votes --with-xunit --with-xcoverage
django-admin.py harvest  --settings=memopol2.testsettings --verbosity=3 -a meps
pylint --rcfile=.pylintrc apps | tee pylint.out
