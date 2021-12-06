import environ
import os

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (scoretrade/config/settings/base.py - 3 = scoretrade/)
APPS_DIR = ROOT_DIR.path("apps")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.bool("DJANGO_DEBUG", False)
DEBUG = env.bool("DJANGO_DEBUG", True)

# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "push_notifications",
    "users.apps.UsersAppConfig",
    "mails.apps.MailsAppConfig",
    "notifications.apps.NotificationsAppConfig",
]

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

ROOT_URLCONF = "config.routers"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ROOT_DIR.path("templates")],
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

ASGI_APPLICATION = "config.asgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {"default": env.db("DATABASE_URL")}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
# DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"
# DATABASES["OPTIONS"] = {"charset": "utf8mb4"}

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(ROOT_DIR, 'localdb'),
}
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "EST"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = "/static/"
STATIC_ROOT = ROOT_DIR.path("staticfiles")


AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}

CLIENT_SECRET_FILE = ROOT_DIR.path("secrets/client_secret.json")


# Push notifications
PUSH_NOTIFICATIONS_SETTINGS = {
    "UPDATE_ON_DUPLICATE_REG_ID": True,
    "CONFIG": "push_notifications.conf.AppConfig",
    "APPLICATIONS": {
        "ios_app": {
            "PLATFORM": "APNS",
            "CERTIFICATE": str(ROOT_DIR.path("certs"))
            + "/"
            + env.str("APNS_CERT_NAME"),
            "TOPIC": env.str("APNS_TOPIC"),
            "USE_SANDBOX": False,
        },
        "android_app": {"PLATFORM": "FCM", "API_KEY": env.str("FCM_API_KEY")},
    },
}


CELERY_BROKER_URL = env("CLOUDAMQP_URL")
CELERY_RESULT_BACKEND = "rpc"


GMAIL_QUERY = env.str("GMAIL_QUERY")
