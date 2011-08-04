# Django settings for memopol2 project.

import os
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# those emails are used as the contact form recipient
ADMINS = (
    ('memopol', 'contact@lqdn.fr'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL='memopol@lqdn.fr'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/%s-memopol2.sqlite' % os.getenv('USER'),
    },
}

APPS_DEBUG = False
if os.getenv('VIRTUAL_ENV'):
    DATABASES['default']['NAME'] = '%s/memopol2.sqlite' % os.getenv('VIRTUAL_ENV')
    APPS_DEBUG = True
elif not os.path.isfile('bin/django-manage'):
    APPS_DEBUG = True


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

MEDIA_DIRECTORY = os.path.join(PROJECT_PATH, MEDIA_URL.lstrip('/'))

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pw93$2vi7^b_8q#-j@z2#2rc-x7e(vcqmi)ekf9%8h57)#caoy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

if APPS_DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
)

ROOT_URLCONF = 'memopol2.urls'


TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

INSTALLED_APPS = (
    # django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.comments',

    # 3rd party
    'south',
    'flatblocks',
    'contact_form',

    # memopol
    'reps',
    'meps',
    'votes',
    'mps',
    'queries',
    'trends',
    'trophies',
)

if APPS_DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
    )

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

LANGUAGES = (
  ('fr', 'French'),
  ('en', 'English'),
)

FIXTURE_DIRS = (
    'fixtures',
)

PARLTRACK_URL = "http://parltrack.memopol2.lqdn.fr"
ROOT_URL = "http://memopol2.lqdn.org"

try:
    from settings_local import *
except ImportError:
    pass
