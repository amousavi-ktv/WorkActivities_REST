"""
Django settings for WorkActivities project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath
from dotenv import load_dotenv, find_dotenv 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b2c3a042-ebf1-4c3b-8f38-981f3b3c84f9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'app',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TimesheetApp',
    'WorkActivities',
    'widget_tweaks',
    'social_django',
    'django_tables2',
    'rest_framework',
]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
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

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'TimesheetApp' / 'templates'], 
        # 'DIRS': [os.path.join(BASE_DIR, 'TimesheetApp', 'templates')],     
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
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_TZ = False
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_L10N = False  # If True, will override the above with locale-specific formats

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

load_dotenv (dotenv_path="../Resources/.env")
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'WorkActivities',
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': 'localhost\SQLSERVER2022',
        'PORT': '1433',  # Default SQL Server port
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',  # Match the installed driver
        },
    }
}
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',  # Google login
    'django.contrib.auth.backends.ModelBackend',

    # 'TimesheetApp.backends.EmailBackend',        # Your email + password form
    # 'django.contrib.auth.backends.ModelBackend', # Optional fallback (admin site, etc.); uncomment if required
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['email', 'name']

# Restrict to company domain
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'hd': 'karbalatv.com'
}


SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',

    'TimesheetApp.pipeline.link_auth_user',  # your custom function / our custom step

    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',  # <-- critical for login
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]

LOGIN_URL = '/auth/login/google-oauth2/?prompt=select_account&hd=karbalatv.com'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = 'https://accounts.google.com/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:8000/'

# LOGIN_URL = '/login/'   # Not /accounts/login/
# LOGIN_REDIRECT_URL = 'dashboard'
# LOGOUT_REDIRECT_URL = '/login/'

# Session expires after 5 minutes (300 seconds)
# SESSION_COOKIE_AGE = 300  

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ALLOWED_HOSTS = ['*']  # for testing, allow all hosts (or use specific IP)
# ALLOWED_HOSTS = ['appserver.karbalatv.com', '10.44.15.1']
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.44.15.1', 'appserver.karbalatv.com']

# Display format
DATE_FORMAT = "d M Y"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "Y/m/d H:i:s"

# Input parsing format
DATE_INPUT_FORMATS = ["%d %b %Y"]
TIME_INPUT_FORMATS = ["%H:%M:%S"]
DATETIME_INPUT_FORMATS = ["%Y/%m/%d %H:%M:%S"]
DATETIME_FORMAT = "Y-m-d H:i:s"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
