cd $WORKSPACE
virtualenv -q ve
source ./ve/bin/activate
pip install -q -E ./ve -r requirements.txt
pip install -q -E ./ve -r requirements-test.txt
python setup.py --quiet develop
django-admin.py test --settings=memopol2.settings.test --with-coverage --cover-package=memopol2 --with-xunit --with-xcoverage
