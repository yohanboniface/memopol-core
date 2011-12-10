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

DEFAULT_FROM_EMAIL = 'memopol@lqdn.fr'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/%s-memopol2.sqlite' % os.getenv('USER'),
    },
}

WHOOSH_INDEX = '/tmp/%s-memopol2.index' % os.getenv('USER')

APPS_DEBUG = False
if os.getenv('VIRTUAL_ENV'):
    DATABASES['default']['NAME'] = '%s/memopol2.sqlite' % os.getenv('VIRTUAL_ENV')
    WHOOSH_INDEX = '%s/memopol2.index' % os.getenv('VIRTUAL_ENV')
    APPS_DEBUG = True
elif not os.path.isfile('bin/django-manage'):
    APPS_DEBUG = True

SNIPPETS_CACHE_DELAY = 3600 * 60 * 24

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
MEDIA_URL = ''

MEDIA_DIRECTORY = ''

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
    'django.middleware.cache.UpdateCacheMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

# WARNING just setting up DEBUG = False in settings_local won't change the cache settings!
ENABLE_CACHING = not DEBUG

CACHES = {
    'default' : dict(
        BACKEND = 'django.core.cache.backends.%s' % ('locmem.LocMemCache' if ENABLE_CACHING else 'dummy.DummyCache'),
        JOHNNY_CACHE = True,
    )
}

JOHNNY_MIDDLEWARE_KEY_PREFIX='cache_memopol2'

if APPS_DEBUG:
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'campaign.context_processor.campaigns',
)

ROOT_URLCONF = 'memopol2.urls'


TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

STATIC_ROOT = os.path.join(PROJECT_PATH, "static_deploy/static")

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, "static"),
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
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'south',
    'flatblocks',
    'contact_form',
    'captcha',

    # memopol
    'reps',
    'meps',
    'votes',
    'mps',
    'queries',
    'trends',
    'trophies',
    'campaign',
    'search',
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

PARLTRACK_URL = "http://parltrack.euwiki.org"
ROOT_URL = "http://memopol2.lqdn.org"

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

try:
    from settings_local import *
except ImportError:
    pass
