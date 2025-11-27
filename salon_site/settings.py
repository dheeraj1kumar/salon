# from pathlib import Path
# from decouple import config
# from datetime import timedelta
# import os
# BASE_DIR = Path(__file__).resolve().parent.parent

# # SECURITY
# SECRET_KEY = config("DJANGO_SECRET_KEY", default="dummysecret")
# # DEBUG = config("DJANGO_DEBUG")


# DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="localhost").split(",")

# # Application definition
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     'dashboard',
#     'user',
#     'booking',
#     'mybooking',
#     'payment',
#     'contact',
#     'assistant',
#     'manager',
# ]

# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "salon_site.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": ['templates'],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "salon_site.wsgi.application"

# # Database (SQLite for demo)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
# ]

# # Custom user
# AUTH_USER_MODEL = "user.CustomUser"

# # Internationalization
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "Asia/Kolkata"
# USE_I18N = True
# USE_TZ = True

# # Static files
# STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []


# STORAGES = {
#     "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
#     "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
# }
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# # Razorpay
# RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID", default="")
# RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET", default="")

# # Gemini
# GEMINI_API_KEY = config("GEMINI_API_KEY", default="")


# # Email
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # Twilio
# TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default="")
# TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default="")
# TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER", default="")

# # Sessions
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SECURE = False

# # Password reset timeout
# PASSWORD_RESET_TIMEOUT = 3600

# # Login
# LOGIN_URL = "/"

# # Custom context processors
# TEMPLATES[0]["OPTIONS"]["context_processors"] += [
#     "booking.context_processors.cart_count",
# ]

# MEDIA_ROOT = BASE_DIR / 'media'
# MEDIA_URL = '/media/'




# 
from pathlib import Path
from decouple import config
import os

# -----------------------------
# Base Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Security Settings
# -----------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dummy_secret_key")

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "13.202.35.125",   # your EC2 public IP
]

# -----------------------------
# Installed Apps
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your apps
    "dashboard",
    "user",
    "booking",
    "mybooking",
    "payment",
    "contact",
    "assistant",
    "manager",
]

# -----------------------------
# Middleware
# -----------------------------
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

ROOT_URLCONF = "salon_site.urls"

# -----------------------------
# Templates
# -----------------------------
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
                "booking.context_processors.cart_count",
            ],
        },
    },
]

WSGI_APPLICATION = "salon_site.wsgi.application"

# -----------------------------
# Database (PostgreSQL)
# -----------------------------
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'salondb',
#         'USER': 'postgres',
#         'PASSWORD': '12345',
#         # 'HOST': 'db',  # <--- works only inside Docker
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }


import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'salondb'),
        'USER': os.environ.get('DB_USER', 'salonuser'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'salonpass'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# -----------------------------
# Custom User Model
# -----------------------------
AUTH_USER_MODEL = "user.CustomUser"

# -----------------------------
# Password Validators
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -----------------------------
# Static & Media
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------
# Third Party API Keys
# -----------------------------
RAZORPAY_KEY_ID = config("RAZORPAY_KEY_ID", default="")
RAZORPAY_KEY_SECRET = config("RAZORPAY_KEY_SECRET", default="")

GEMINI_API_KEY = config("GEMINI_API_KEY", default="")

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", default="")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", default="")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER", default="")

# -----------------------------
# Email (SMTP - Gmail)
# -----------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -----------------------------
# Sessions & Security
# -----------------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = config("DJANGO_SESSION_SECURE", default=False, cast=bool)

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = config("DJANGO_CSRF_SECURE", default=False, cast=bool)

# -----------------------------
# Password Reset
# -----------------------------
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour

# -----------------------------
# Login
# -----------------------------
LOGIN_URL = "/"
