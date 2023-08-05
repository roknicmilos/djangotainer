from .common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'run', 'dev.sqlite3'),
    }
}

INSTALLED_APPS = DEFAULT_APPS
