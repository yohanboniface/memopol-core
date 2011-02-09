#!/bin/sh
django-admin.py test --settings=memopol2.testsettings --with-coverage --cover-package=memopol2 --with-xunit --with-xcoverage
pylint --rcfile=.pylintrc memopol2 | tee pylint.out
