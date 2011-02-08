#!/bin/bash
# This script will setup our virtualenv in the jenkins workspace, and run the tests

cd $WORKSPACE

# setup ve
virtualenv --no-site-packages --distribute -q ve
source ./ve/bin/activate

# dev install - installs requirements as well
python setup.py --quiet develop

# add our test requirements
pip install -q -E ./ve -r requirements-test.txt

# run our tests
source ./bin/run-all-tests.sh
