#!/usr/bin/env python
import sys, os.path
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path = [os.path.join(BASE_PATH, 'apps'),] + sys.path
from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory. pylint: disable=W0403
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__) # pylint: disable=C0301
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
