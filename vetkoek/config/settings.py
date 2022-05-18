from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "63j9UNXJW8S5Rk1nfk+OI2HtFcodiUDRAfyvVe3tdczODHpg6OTv5dzaixmNAkH9Y3KeEPi/HCmZnEKTact/7wZL4aN//RzY"

DEBUG = True

ALLOWED_HOSTS = [
    "msukwini.com",
    "www.msukwini.com",
    "127.0.0.1",
    "localhost",
    "157.245.249.4",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third-party apps
    "captcha",
    "corsheaders",
    "imagekit",
    "storages",
    # ViSpace apps
    "vetkoek.core",
    "vetkoek.core.accounts",
    "vetkoek.core.communities",
    "vetkoek.core.posts",
    "vetkoek.core.search",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
]

ROOT_URLCONF = "vetkoek.config.urls"

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

WSGI_APPLICATION = "vetkoek.config.wsgi.application"

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
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "msukwini",
            "USER": "samkelo",
            "PASSWORD": "Jm218071748*",
            "HOST": "localhost",
            "PORT": "",
        }
    }

AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = ["vetkoek.core.accounts.backends.EmailBackend"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Johannesburg"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "/u/login/"

LOGIN_REDIRECT_URL = "/f/"

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

HTML_MINIFY = True

RECAPTCHA_PUBLIC_KEY = "6LfL3VwbAAAAAAjNlajN06IQU5kM0ZBdgS_nZHp-"

RECAPTCHA_PRIVATE_KEY = "6LfL3VwbAAAAAG-5AcpAiGmitRwRkE2oabWlnZJB"

RECAPTCHA_REQUIRED_SCORE = 0.85

REST_FRAMEWORK = {
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

if not DEBUG:
    AWS_ACCESS_KEY_ID = "AKO5SR4NSE42JDWTA75I"

    AWS_SECRET_ACCESS_KEY = "L2Oc2iyNlahEEnqitrAyOOsglQhFQIQDtvxr2Ll2dFg"

    AWS_STORAGE_BUCKET_NAME = "msukwini-images"

    AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"

    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    AWS_LOCATION = "msukwini-media"

    STATIC_URL = "https://%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)

    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "config.storage_backends.PublicMediaStorage"

else:
    STATIC_URL = "static/"
    STATICFILES_DIRS = [BASE_DIR / "_static"]
    MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "static"
