import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def load_local_env(env_path):
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


load_local_env(BASE_DIR / ".env")


def to_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def to_csv_list(value, default=""):
    source = default if value is None else value
    return [item.strip() for item in str(source).split(",") if item.strip()]


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-it-coursework-local-only")
DEBUG = to_bool(os.environ.get("DJANGO_DEBUG"), default=True)
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID", "").strip()
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET", "").strip()
GOOGLE_OAUTH_ENABLED = bool(GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET)

MICROSOFT_OAUTH_CLIENT_ID = os.environ.get("MICROSOFT_OAUTH_CLIENT_ID", "").strip()
MICROSOFT_OAUTH_CLIENT_SECRET = os.environ.get("MICROSOFT_OAUTH_CLIENT_SECRET", "").strip()
MICROSOFT_OAUTH_TENANT = os.environ.get("MICROSOFT_OAUTH_TENANT", "organizations").strip()
MICROSOFT_OAUTH_ENABLED = bool(MICROSOFT_OAUTH_CLIENT_ID and MICROSOFT_OAUTH_CLIENT_SECRET)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.microsoft",
    "core",
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

ROOT_URLCONF = "it_site.urls"

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
                "core.context_processors.social_auth_context",
            ],
        },
    },
]

WSGI_APPLICATION = "it_site.wsgi.application"
ASGI_APPLICATION = "it_site.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ENABLE_HTTPS = to_bool(os.environ.get("DJANGO_ENABLE_HTTPS"), default=not DEBUG)

if ENABLE_HTTPS:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = int(os.environ.get("DJANGO_SITE_ID", "1"))

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
            "prompt": "select_account",
        },
        **(
            {
                "APP": {
                    "client_id": GOOGLE_OAUTH_CLIENT_ID,
                    "secret": GOOGLE_OAUTH_CLIENT_SECRET,
                    "key": "",
                }
            }
            if GOOGLE_OAUTH_ENABLED
            else {}
        ),
    },
    "microsoft": {
        "SCOPE": ["User.Read"],
        "AUTH_PARAMS": {
            "prompt": "select_account",
        },
        "TENANT": MICROSOFT_OAUTH_TENANT,
        **(
            {
                "APP": {
                    "client_id": MICROSOFT_OAUTH_CLIENT_ID,
                    "secret": MICROSOFT_OAUTH_CLIENT_SECRET,
                    "key": "",
                }
            }
            if MICROSOFT_OAUTH_ENABLED
            else {}
        ),
    },
}

SOCIALACCOUNT_ADAPTER = "core.adapters.DomainRestrictedSocialAccountAdapter"
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIAL_ALLOWED_EMAIL_DOMAINS = [
    domain.lower()
    for domain in to_csv_list(
        os.environ.get("DJANGO_SOCIAL_ALLOWED_EMAIL_DOMAINS"),
        default="glasgow.ac.uk,student.gla.ac.uk",
    )
]
SOCIAL_DOMAIN_RESTRICTED_PROVIDERS = [
    provider.lower()
    for provider in to_csv_list(
        os.environ.get("DJANGO_SOCIAL_DOMAIN_RESTRICTED_PROVIDERS"),
        default="microsoft",
    )
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
