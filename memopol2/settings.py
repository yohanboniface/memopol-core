# Django settings for memopol2 project.

import os
from os.path import join, exists
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
SUBPROJECT_PATH = os.path.split(PROJECT_PATH)[0]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# those emails are used as the contact form recipient
ADMINS = (
    ('memopol', 'contact@lqdn.fr'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'memopol@lqdn.fr'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/memopol2.sqlite' % PROJECT_PATH,
    },
}

WHOOSH_INDEX = '%s/memopol2.index' % PROJECT_PATH

APPS_DEBUG = False
if os.getenv('VIRTUAL_ENV'):
    DATABASES['default']['NAME'] = '%s/memopol2.sqlite' % PROJECT_PATH
    WHOOSH_INDEX = '%s/memopol2.index' % PROJECT_PATH
    APPS_DEBUG = True
elif not os.path.isfile('bin/django-manage'):
    APPS_DEBUG = True

SNIPPETS_CACHE_DELAY = 3600 * 60 * 24

ORGANIZATION_NAME = "La Quadrature du Net"

MEMOPOL_TMP_DIR = join(SUBPROJECT_PATH, "tmp")

if not exists(MEMOPOL_TMP_DIR):
    os.makedirs(MEMOPOL_TMP_DIR)

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
# FIXME: change it when MEDIA_DIRECTORY stuff is FIXED
MEDIA_URL = '/medias/'

# FIXME: remove this setting, use MEDIA_ROOT instead
MEDIA_DIRECTORY = os.path.join(PROJECT_PATH, MEDIA_URL.lstrip('/'))

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pw93$2vi7^b_8q#-j@z2#2rc-x7e(vcqmi)ekf9%8h57)#caoy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

if APPS_DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

# WARNING just setting up DEBUG = False in settings_local won't change the cache settings!
ENABLE_CACHING = not DEBUG

CACHES = {
    'default' : dict(
        BACKEND = 'django.core.cache.backends.%s' % ('locmem.LocMemCache' if ENABLE_CACHING else 'dummy.DummyCache'),
        OPTIONS = {
            'MAX_ENTRIES': 1000000000,
        }
    )
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    #'campaign.context_processor.campaigns',
)

ROOT_URLCONF = 'memopol2.urls'


TEMPLATE_DIRS = (
    os.path.join(SUBPROJECT_PATH, "templates"),
)

STATIC_ROOT = os.path.join(PROJECT_PATH, "static_deploy/static")

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "static"),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

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
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'flatblocks',
    'contact_form',
    'captcha',
    'django_extensions',
    'memopol2',
    'reps',
    'meps',
    'votes',
    'mps',
    'trends',
    'trophies',
    'campaign',
    'parltrack',
    'search',
    'gunicorn',
    'positions',
    'haystack',
    'ajax_select',
    'dynamiq',
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
    'debug_toolbar.panels.state.StateDebugPanel',
    'debug_toolbar.panels.htmlvalidator.HTMLValidationDebugPanel',
)

LANGUAGES = (
  ('fr', 'French'),
  ('en', 'English'),
)

LOCALE_PATHS = (
    SUBPROJECT_PATH + '/locale',
)

FIXTURE_DIRS = (
    'fixtures',
)

PARLTRACK_URL = "http://parltrack.euwiki.org"
ROOT_URL = "https://memopol.lqdn.fr"

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'memopol2': {
            'handlers': ['console'],
            'level': 'WARN',
            'propagate': True,
        },
        'search': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

COMMENTS_APP = 'positions'

WHOOSH_TEMPORARY_INDEX = '%s/temporary.index' % PROJECT_PATH
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_TEMPORARY_INDEX,
    },
}
HAYSTACK_DOCUMENT_FIELD = "fulltext"
AJAX_LOOKUP_CHANNELS = {
    # dynamiq_search is a "fake" channel, it's used to dynamically switch channels
    # in javascript - the widget needs a real one to start with something...
    'dynamiq_search': ('dynamiq.ajax_lookups', 'DynamiqAjaxLookupSearch'),
}

try:
    from settings_local import *
except ImportError:
    pass
