# Django settings for rippleeffect project.

import os
from django.core.exceptions import ImproperlyConfigured

def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

# DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DEBUG = True

if os.environ.get('RIPPLE_PRODUCTION', False):
    DEBUG = False

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alper Cugun', ''),
)

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

SERVER_EMAIL = ""

MANAGERS = ADMINS

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(os.path.dirname(SITE_ROOT), 'ripple.db'),                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': '',
            'PASSWORD': '',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'techtrialnew',
            'USER': 'techtrialnew',
            'PASSWORD': '',
            'HOST': '',          
            'PORT': '',
        }
    }

if os.environ.get('RIPPLEEFFECT_ENV', None) == 'STAGING':
    DEBUG = False
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'staging',
            'USER': 'staging',
            'PASSWORD': get_env_setting('RIPPLEEFFECT_MYSQL_PASSWORD'),
            'HOST': '',          
            'PORT': '',
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.playrippleeffect.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'staticroot')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"riskgame.context_processors.player")

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'riskgame.middleware.WWWRedirectMiddleware',
    'riskgame.middleware.ImpersonateMiddleware'
]

ROOT_URLCONF = 'rippleeffect.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rippleeffect.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    
    'riskgame',
    'nousernameregistration',
    'south',
    'crispy_forms',
#    'registration',

    # celery async task queue
    'djcelery',
    'django_nose',
    # 'debug_toolbar'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379:1',
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser'
        }
    }
}


CRISPY_TEMPLATE_PACK = 'bootstrap'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SOUTH_TESTS_MIGRATE = False

AUTH_USER_MODEL = 'riskgame.EmailUser'

# Settings for django-registration

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/signin/'
# LOGOUT_URL = '/signout/'


# E-mail settings
DEFAULT_FROM_EMAIL = ''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = '587'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True


# Settings for django-passwords
PASSWORD_COMMON_SEQUENCES = []

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# celery settings
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}  # 1 hour.

if not DEBUG:
    CELERY_SEND_TASK_ERROR_EMAILS = True

from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    "change-days": {
        "task": "riskgame.tasks.change_days",
        "schedule": crontab(minute="*/1")
    },
    # "test-task": {
    #     "task": "riskgame.tasks.test_task",
    #     "schedule": crontab(minute="*/1")
    # }
}

# Celery async task queue settings
import djcelery
djcelery.setup_loader()
