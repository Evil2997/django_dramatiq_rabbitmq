import logging
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-10uc5&x9zpb-+awc_zou&@oldzbovf##838vy@pvb!08^+%ecw"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'django_dramatiq',
    "app3",

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

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

BROKER_URL = "amqp://guest:guest@rabbitmq:5672/"

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": BROKER_URL,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "django_dramatiq.middleware.AdminMiddleware",
    ]
}

WSGI_APPLICATION = "myproject.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose"
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'dramatiq_tasks.log',
            'formatter': 'verbose',
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] "
                      "[PID %(process)d] "
                      "[Thread %(thread)d] "
                      "[%(module)s] "
                      "[%(levelname)s] "
                      ": %(message)s "
                      "(%(filename)s:%(lineno)d)",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'dramatiq': {  # Логгер для библиотеки Dramatiq
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'app3': {  # Логгер для вашего приложения
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
            "COLOR": "#123123"
        },
    },
}
