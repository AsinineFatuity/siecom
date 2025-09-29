import os
import sys
import logging
import dj_database_url
from pathlib import Path
from decouple import config
from siecom.utils import get_environment, PROD_ENVIRONMENT
from huey import RedisHuey

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
TO_SET_WARNING_LOGGING_LEVEL = ["factory", "faker", "urllib3"]
for logger_name in TO_SET_WARNING_LOGGING_LEVEL:
    logging.getLogger(logger_name).setLevel(logging.WARNING)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY")
ENVIRONMENT = get_environment()
DEBUG = 0 if ENVIRONMENT == PROD_ENVIRONMENT else 1
USE_DOCKER = config("USE_DOCKER", default=0, cast=int)
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
    "http://174.138.123.164",
]

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

PROJECT_APPS = ["core"]
THIRD_PARTY_APPS = [
    "phonenumber_field",
    "graphene_django",
    "tree_queries",
    "huey.contrib.djhuey",
    "django_extensions",
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "siecom.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "siecom.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DB_URL = config("DOCKER_DB_URL") if USE_DOCKER else config("DATABASE_URL")

DATABASES = {"default": dj_database_url.parse(DB_URL, conn_max_age=600)}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "core.User"

GRAPHENE_MIDDLEWARES = [
    "siecom.middleware.OIDCAuthenticationMiddleware",
]
if not DEBUG:
    GRAPHENE_MIDDLEWARES.append(
        "siecom.middleware.GrapheneBlockIntrospectionMiddleware"
    )

GRAPHENE = {
    "SCHEMA": "siecom.schema.schema",
    "ATOMIC_MUTATIONS": True,
    "MIDDLEWARE": GRAPHENE_MIDDLEWARES,
}
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = "/home/app/staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REDIS_HOST = "redis" if USE_DOCKER else "localhost"
HUEY = RedisHuey(
    "siecom",
    host=REDIS_HOST,
    port=6379,
    db=0,
)
