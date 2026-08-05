"""
Django settings for backend project.
"""

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------
# SECURITY
# -----------------------------------------------------

SECRET_KEY = "django-insecure-99sferd!v1qhxz1z8qe)cdn82+wga$8wr2^6cp)t&h9cft$0pe"

DEBUG = True

ALLOWED_HOSTS = ["*"]   # Change in production

# -----------------------------------------------------
# INSTALLED APPS
# -----------------------------------------------------

INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party Apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "channels",

    # Local Apps
    "accounts.apps.AccountsConfig",
    "ingestion",
    "alerts",
    "detection",
    "api",
    "investigations",
]

# -----------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------
# URLS
# -----------------------------------------------------

ROOT_URLCONF = "backend.urls"

# -----------------------------------------------------
# Templates
# -----------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# -----------------------------------------------------
# WSGI / ASGI
# -----------------------------------------------------

WSGI_APPLICATION = "backend.wsgi.application"

# FIXED (yours was incorrect)
ASGI_APPLICATION = "backend.asgi.application"

# -----------------------------------------------------
# DATABASE
# -----------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "logmonitor",
        "USER": "root",
        "PASSWORD": "admin@123",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

# -----------------------------------------------------
# PASSWORD VALIDATORS
# -----------------------------------------------------

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

# -----------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# -----------------------------------------------------
# STATIC FILES
# -----------------------------------------------------

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------
# CORS
# -----------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True

# -----------------------------------------------------
# DRF
# -----------------------------------------------------

REST_FRAMEWORK = {

   "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    # Pagination
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",

    "PAGE_SIZE": 10,
}

# -----------------------------------------------------
# JWT SETTINGS
# -----------------------------------------------------

SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),

    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": False,

    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",

    "SIGNING_KEY": SECRET_KEY,

    "AUTH_HEADER_TYPES": ("Bearer",),

    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),
}

# -----------------------------------------------------
# CHANNELS
# -----------------------------------------------------

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# -----------------------------------------------------
# CELERY
# -----------------------------------------------------

CELERY_BEAT_SCHEDULE = {
    "run-siem-every-5-seconds": {
        "task": "logs.tasks.run_detection_engine",
        "schedule": 5.0,
    }
}