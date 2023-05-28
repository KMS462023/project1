import os
import dj_database_url
import dotenv

from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


DEBUG = False

ALLOWED_HOSTS = ["*",]  # since Telegram uses a lot of IPs for webhooks


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    # 3rd party apps
    'django_celery_beat',
    # local apps
     'info.apps.InfoConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
]

X_FRAME_OPTIONS = 'ALLOWALL'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'inmain.urls'

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

WSGI_APPLICATION = 'inmain.wsgi.application'
# ASGI_APPLICATION = 'inmain.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

 DATABASES = {
     'default': {
         'ENGINE': os.getenv('SQL_ENGINE'),
         'NAME': os.getenv('SQL_DATABASE'),
         'USER': os.getenv('SQL_USER'),
         'PASSWORD': os.getenv('SQL_PASSWORD'),
         'HOST': os.getenv('SQL_HOST'),
         'PORT': os.getenv('SQL_PORT'),
     }
 }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'inmain/static'),
]

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')


AWS_S3_CUSTOM_DOMAIN = 'storage.yandexcloud.net/medva'
AWS_S3_REGION_NAME = 'ru-central1'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = ''
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://'storage.yandexcloud.net/medva/"
MEDIA_URL = "https://storage.yandexcloud.net/medvamedia/"
AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
DEFAULT_FILE_STORAGE = 'inmain.storage_backends.MediaStorage'  # <-- here is where we reference i


# # -----> CELERY
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_DEFAULT_QUEUE = 'medva_celery'


EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.beget.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'account@medva.ru'
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'account@medva.ru'
DEFAULT_TO_EMAIL = 'account@medva.ru'
SERVER_EMAIL = "account@medva.ru"

# -----> TELEGRAM
#TELEGRAM_TOKEN = "5054664856:AAGBnXKFldnJT4QMkO1kuE02Pm42ZbBxX3o"
#TELEGRAM_TOKEN2 = "5089794195:AAFDvFgexfj09jDf__WyCEkJVCiksGR9Qms"


# -----> LOGGING
ENABLE_DECORATOR_LOGGING = os.getenv('ENABLE_DECORATOR_LOGGING', True)


# -----> SENTRY
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.celery import CeleryIntegration
# from sentry_sdk.integrations.redis import RedisIntegration

# sentry_sdk.init(
#     dsn="INPUT ...ingest.sentry.io/ LINK",
#     integrations=[
#         DjangoIntegration(),
#         CeleryIntegration(),
#         RedisIntegration(),
#     ],
#     traces_sample_rate=0.1,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )

