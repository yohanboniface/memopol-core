"""pylint option block-disable-msg"""

from memopol2.settings import * # pylint: disable=W0614,W0401

#ROOT_URLCONF = 'yourapp.settings.test.urls'
#DATABASE_ENGINE = 'sqlite3'
#DATABASE_NAME = ':memory:'

INSTALLED_APPS += ('django_nose', )
TEST_RUNNER = 'django_nose.run_tests'
