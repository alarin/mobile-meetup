#encoding: utf-8

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(PROJECT_PATH, 'apps'));

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Anatoly Larin', 'me@alarin.ru'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru'
LANGUAGES = ('ru', 'Russian'),

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'files/upload/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'files/static/')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'dsdsdskwejkewjewkjrkwjfsdknskdfn$#(@#($R%*($*rfsidjjdnvjfrwefdsc'

TEMPLATE_LOADERS = (
    'dbtemplates.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'anticms.middleware.MenuMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages",
    'anticms.context_processors.menu',
)

AUTHENTICATION_BACKENDS  = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates/'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
### Tools
    'south',
    'dbtemplates',
    'reversion',
    'mptt',
    'treemenus',
    'anticms',
    'epio',
### Apps
    'sorl.thumbnail',
    'core',
    'conference',
    'mm_core',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django',
    },
}
CACHES['dbtemplates'] = CACHES['default']

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

DBTEMPLATES_CACHE_BACKEND = 'dbtemplates.cache.DjangoCacheBackend'
DBTEMPLATES_USE_REVERSION = True
DBTEMPLATES_USE_CODEMIRROR = True

GOOGLE_ANALYTICS_CODE = ''
DATETIME_FORMAT = 'd.m.Y G:i'

try:
    from settings_local import *
except ImportError:
    pass