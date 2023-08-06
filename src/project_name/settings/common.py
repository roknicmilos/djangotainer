import os
from os.path import abspath, basename, dirname, join, normpath
import sys

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

PROJECT_ROOT = dirname(DJANGO_ROOT)

SITE_NAME = basename(DJANGO_ROOT)

STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps:
    'django_extensions',

    # Custom apps:
    'apps.common',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

USE_I18N = False

USE_TZ = False

SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key')  # TODO

ADMINS = (
    ('your name', 'your_name@example.com'),  # TODO (emails should not be sent)
)

MANAGERS = ADMINS

WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

ROOT_URLCONF = '%s.urls' % SITE_NAME

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

DEBUG = False

AUTH_USER_MODEL = "users.User"
