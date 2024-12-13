import stripe
from pathlib import Path
from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / "subdir".

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config("SECRET_KEY")


# SECURITY WARNING: don"t run with debug turned on in production!

DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "tailwind",
    "theme",

    "apps.home",
    "apps.account",
    "apps.payment",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "NAME": config("DB_NAME"),
        }
    }

# Password validation

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

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static/"

STATICFILES_DIRS = [BASE_DIR / "theme/static/"]

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media/"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# TailwindCSS

TAILWIND_APP_NAME = "theme"

INTERNAL_IPS = ["127.0.0.1"]

NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"


# User Model

AUTH_USER_MODEL = "account.User"

AUTHENTICATION_BACKENDS = ["apps.account.backends.CustomBackend"]

SESSION_COOKIE_AGE = 86400

LOGIN_URL = "entrar/"


# Email

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

EMAIL_HOST = config("EMAIL_HOST")

EMAIL_PORT = config("EMAIL_PORT")

EMAIL_USE_TLS = True


# Stripe

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")

STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")

STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")

stripe.api_key = STRIPE_SECRET_KEY


# Jazzmin

JAZZMIN_SETTINGS = {
    "welcome_sign": "Seja bem vindo",
    "site_brand": "Empresa",
}
