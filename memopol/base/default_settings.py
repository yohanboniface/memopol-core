# -*- coding:utf-8 -*-
#==============================================================================
# MEMOPOL CORE DEFAULT SETTINGS
# Store here only the memopol apps settings
# Project specific settings must be in the projects
#==============================================================================

from django.conf.global_settings import *   # pylint: disable=W0614,W0401

import os
MEMOPOL_BASE_PATH = os.path.abspath(os.path.split(__file__)[0])
MEMOPOL_PATH = os.path.split(MEMOPOL_BASE_PATH)[0]

#==============================================================================
# Generic Django project settings
#==============================================================================

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
    'memopol.base',
    'memopol.reps',
    'memopol.meps',
    'memopol.votes',
    'memopol.mps',
    'memopol.trends',
    'memopol.trophies',
    'memopol.campaign',
    'memopol.parltrack',
    'memopol.nosdeputes',
    'memopol.search',
    'gunicorn',
    'memopol.positions',
    'haystack',
    'ajax_select',
    'dynamiq',
    'memopol.patch_o_maton',
    'categories',
    'categories.editor',
    'endless_pagination',
    'compressor',
)
STATICFILES_FINDERS += (
    "compressor.finders.CompressorFinder",
)
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)
CACHE_MIDDLEWARE_SECONDS = 60 * 60  # one hour
MIDDLEWARE_CLASSES = (
    'memopol.base.middlewares.CacheControlHeaders',  # Must be first to be
                                                     # last while processing
                                                     # response
    ) + MIDDLEWARE_CLASSES

#==============================================================================
# Memopol core default settings
#==============================================================================
SNIPPETS_CACHE_DELAY = 3600 * 60 * 24
ORGANIZATION_NAME = "La Quadrature du Net"
PARLTRACK_URL = "http://parltrack.euwiki.org"
ROOT_URL = "https://memopol.lqdn.fr"
APPS_DEBUG = DEBUG  # FIXME: remove


#==============================================================================
# Third party app settings
#==============================================================================
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
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'memopol.search.backends.WhooshEngine',
        'PATH': 'memopol2.index',
    },
}
HAYSTACK_DOCUMENT_FIELD = "fulltext"
AJAX_LOOKUP_CHANNELS = {
    # dynamiq_search is a "fake" channel, it's used to dynamically switch channels
    # in javascript - the widget needs a real one to start with something...
    'dynamiq_search': ('dynamiq.ajax_lookups', 'DynamiqAjaxLookupSearch'),
    'mep_achievements': ('search.ajax_lookups', 'MepAchievements'),
}
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)
COMPRESS_OFFLINE = True
TEMPLATE_LOADERS = (
    'hamlpy.template.loaders.HamlPyFilesystemLoader',
    'hamlpy.template.loaders.HamlPyAppDirectoriesLoader',
) + TEMPLATE_LOADERS

COMMENTS_APP = 'memopol.positions'
