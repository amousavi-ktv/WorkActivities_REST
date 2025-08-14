"""
Django settings for WorkActivities project.
Based on 'django-admin startproject'.
"""

import os
import posixpath
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
# BASE_DIR -> E:\AppServer\Applications\WorkActivities_REST
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Resources is a SIBLING of WorkActivities_REST:
# E:\AppServer\Applications\Resources
RESOURCES_DIR = os.path.join(os.path.dirname(BASE_DIR), "Resources")

# Load env from the external Resources folder
load_dotenv(os.path.join(RESOURCES_DIR, ".env"))

# -----------------------------------------------------------------------------
# Core
# -----------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True

# Keep your existing hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.44.15.1', 'appserver.karbalatv.com']

# -----------------------------------------------------------------------------
# Installed apps
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'app',                  # your legacy app reference
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TimesheetApp',
    'WorkActivities',       # keep if you had templates/static inside project pkg
    'widget_tweaks',
    'social_django',
    'django_tables2',
    'rest_framework',
]

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'TimesheetApp.middleware.ForceGoogleAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WorkActivities.urls'

# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # You previously left DIRS empty; keeping as-is
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'WorkActivities.wsgi.application'

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
# Your original SQLite (kept for reference; immediately overridden below)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Your working MSSQL override (unchanged except for raw string on HOST)
# Make sure DB_USER and DB_PASS exist in your Resources/.env
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'WorkActivities',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': r'localhost\SQLSERVER2022',   # raw string avoids backslash issues
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            # 'extra_params': 'TrustServerCertificate=yes',  # if needed locally
        },
    }
}

# -----------------------------------------------------------------------------
# Password validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# -----------------------------------------------------------------------------
# I18N / TZ
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
USE_TZ = False
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_L10N = False

# -----------------------------------------------------------------------------
# Static
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

# -----------------------------------------------------------------------------
# Authentication & Social (fixed syntax)
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',   # Google login
    'TimesheetApp.backends.EmailBackend',         # your custom backend
    'django.contrib.auth.backends.ModelBackend',
]

# Use Google popup by default (you can add &hd=karbalatv.com if desired)
LOGIN_URL = '/auth/login/google-oauth2/?prompt=select_account'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = 'https://accounts.google.com/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8000/'

# These must be set in your Resources/.env
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=<client_id>
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=<client_secret>
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['email', 'name']

# Restrict to company domain (your previous behavior)
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'hd': 'karbalatv.com'
}

# Social pipeline (kept as-is from your previous file)
SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'TimesheetApp.pipeline.link_auth_user',   # your custom hook
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',  # required for login
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]

# -----------------------------------------------------------------------------
# Sessions / Formats / REST
# -----------------------------------------------------------------------------
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

DATE_FORMAT = "d M Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "Y/m/d H:i:s"
DATE_INPUT_FORMATS = ["%d %b %Y"]
TIME_INPUT_FORMATS = ["%H:%M:%S"]
DATETIME_INPUT_FORMATS = ["%Y/%m/%d %H:%M:%S"]
DATETIME_FORMAT = "Y-m-d H:i:s"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
