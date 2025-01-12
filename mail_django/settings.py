"""
Django settings for mail_django project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config, Csv  # python decouple
from functools import partial  # used in postgrest configuration
import dj_database_url
import sentry_sdk  # Sentry
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# user model

AUTH_USER_MODEL = 'base.User'

# auth urls (set this when you use a different path in url "django.contrib.auth.urls")

LOGIN_REDIRECT_URL = '/logado'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/usuario/login/'
# this will be used when an unauthenticated user tries to access a view where login is required

# Application definition

INSTALLED_APPS = [       # your apps must come first
    'mail_django.base',
    'mail_django.mail_register',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'collectfast',  # collectfast come first that 'django.contrib.staticfiles'
    'django.contrib.staticfiles',
    'ordered_model',
    'django_extensions',
    'anymail',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mail_django.urls'

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

WSGI_APPLICATION = 'mail_django.wsgi.application'


# Django Debug Toolbar
INTERNAL_IPS = config('INTERNAL_IPS', cast=Csv(), default='127.0.0.1')
if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

default_db_url = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

# partial serve para criar uma nova chamada de função personalizada(com alguns parametros preselecionados).
parse_database = partial(dj_database_url.parse, conn_max_age=600)

DATABASES = {
    'default': config('DATABASE_URL', default=default_db_url, cast=parse_database)
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

CONNECTFAST_ENABLED = False

# storage configuration in S3 AWS

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')

if AWS_ACCESS_KEY_ID:  # pragma: no cover
    CONNECTFAST_ENABLED = True
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"  # essa e a anterior sao o do collectfast
    INSTALLED_APPS.append('s3_folder_storage')
    INSTALLED_APPS.append('storages')  # adicionar essas libs apenas se estiver com AWS configurado.
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400', }  # controle de tempo de cach do S3
    AWS_PRELOAD_METADATA = True
    AWS_AUTO_CREATE_BUCKET = False  # nao vamos criar buckets automaticamente
    AWS_QUERYSTRING_AUTH = True  # para gerar urls assinadas.
    AWS_S3_CUSTOM_DOMAIN = None  # por q nos vamos utilizar o proprio dominio do S3
    AWS_DEFAULT_ACL = 'private'  # para que nossos arquivos do S3 nao fiquem publicos.

    # ---/Upload Media Folder

    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    # classe dessa biblioteca que vai fazer a gestão de upload de midia
    DEFAULT_S3_PATH = 'media'  # path padrão dos arquivos de midia.
    MEDIA_ROOT = f'/{DEFAULT_S3_PATH}/'
    MEDIA_URL = f'//{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{DEFAULT_S3_PATH}/'  # '//' vai seguir https ou http

    # -----/Static assets

    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    # classe da biblioteca que instalamos que vai fazer a gestão da pasta static.
    STATIC_S3_PATH = 'static'  # path padrão dos arquivos estaticos
    STATIC_ROOT = f'/{STATIC_S3_PATH}/'
    STATIC_URL = f'//{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{STATIC_S3_PATH}/'
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'  # separar os arquivos staticos de admin


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sentry config

SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
