"""
Django settings for linksight project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import environ

# Load .env file
env = environ.Env(
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost']),
    APPROVED_EMAILS_ROW_KEY=(str, None),
    APPROVED_EMAILS_SHEET_ID=(str, None),
    APPROVED_EMAILS_SHEET_RANGE=(str, None),
    CELERY_BROKER_URL=(str, 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=(str, 'redis://localhost:6379/0'),
    DEBUG=(bool, False),
    EMAIL_HOST_PASSWORD=(str, None),
    EMAIL_HOST_USER=(str, None),
    EMAIL_PORT=(int, 25),
    HOST=(str, 'http://localhost:3000'),
    LOGIN_REDIRECT_URL=(str, 'http://localhost:3000/upload'),
    SENTRY_DSN=(str, None),
    GOOGLE_OAUTH2_KEY=(str, None),
    GOOGLE_OAUTH2_SECRET=(str, None),
)
env.read_env('.env')

HOST = env('HOST')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'linksight.accounts.apps.AccountsConfig',
    'linksight.api',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'raven.contrib.django.raven_compat',
    'silk',
    'registration',
    'social_django',
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linksight.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'linksight.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'app/build/static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files (Uploads)

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'linksight'
GS_PROJECT_ID = 'linksight-208514'
GS_DEFAULT_ACL = 'publicRead'
GS_FILE_OVERWRITE = False

# django-cors-headers

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'linksight.thinkingmachin.es',
)
CORS_ALLOW_CREDENTIALS = True

# DRF

REST_FRAMEWORK = {
    'PAGE_SIZE': 10000,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'linksight.api.authentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
SILENCED_SYSTEM_CHECKS = [
    'rest_framework.W001',
]

# Raven

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN'),
}

# Silk

SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True
SILKY_PERMISSIONS = lambda user: user.is_superuser

# Registration

LOGIN_REDIRECT_URL = env('LOGIN_REDIRECT_URL')
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_ADMINS = [
    ('Steve', 'marksteve@thinkingmachin.es'),
    ('Pia', 'pia@thinkingmachin.es'),
    ('Dani', 'danielle@thinkingmachin.es'),
]
REGISTRATION_FORM = 'linksight.accounts.forms.RegistrationWithSurveyForm'

# Email

DEFAULT_FROM_EMAIL = 'linksight@thinkingmachin.es'
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = 'smtp.mailgun.org'
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Social Auth

SOCIAL_AUTH_POSTGRES_JSONFIELD = True
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['thinkingmachin.es']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'linksight.pipeline.auth_allowed',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.user.user_details',
)

# Approved emails

APPROVED_EMAILS_SHEET_ID = env('APPROVED_EMAILS_SHEET_ID')
APPROVED_EMAILS_SHEET_RANGE = env('APPROVED_EMAILS_SHEET_RANGE')
APPROVED_EMAILS_ROW_KEY = env('APPROVED_EMAILS_ROW_KEY')

# Celery

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_TASK_TIME_LIMIT = 360

