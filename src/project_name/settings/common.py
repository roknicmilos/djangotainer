import sys
from copy import deepcopy
from decouple import config
from django.utils.log import DEFAULT_LOGGING
from os.path import abspath, basename, dirname, join, normpath

DJANGO_ROOT = dirname(dirname(abspath(__file__)))

PROJECT_ROOT = dirname(DJANGO_ROOT)

SITE_NAME = basename(DJANGO_ROOT)

STATIC_ROOT = join(PROJECT_ROOT, "run", "static")

MEDIA_ROOT = join(PROJECT_ROOT, "run", "media")

STATICFILES_DIRS = [
    join(PROJECT_ROOT, "static"),
]

PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, "templates"),
]

sys.path.append(normpath(join(PROJECT_ROOT, "apps")))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": PROJECT_TEMPLATES,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

USE_I18N = False

USE_TZ = False

SECRET_KEY = config("SECRET_KEY")

WSGI_APPLICATION = "%s.wsgi.application" % SITE_NAME

ROOT_URLCONF = "%s.urls" % SITE_NAME

STATIC_URL = "/static/"

MEDIA_URL = "/media/"

DEBUG = config("DEBUG", default=False, cast=bool)

AUTH_USER_MODEL = "users.User"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USERNAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOSTNAME", default="postgres"),
        "PORT": config("DB_PORT", default=5432, cast=int),
    }
}

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default=None)
EMAIL_PORT = config("EMAIL_PORT", default=None, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default=None)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=None, cast=bool)

# Disable error emails:
#   - based on: https://lincolnloop.com/insights/disabling-error-emails-django/
logging_dict = deepcopy(DEFAULT_LOGGING)
logging_dict["loggers"]["django"]["handlers"] = ["console"]
LOGGING = logging_dict
