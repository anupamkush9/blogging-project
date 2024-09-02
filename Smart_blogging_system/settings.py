"""
Django settings for Smart_blogging_system project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i(j3oaf-nyj$moi&m6*km4wkh($^7&b(40jl+1s^7gg1hx%!94'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'froala_editor',
    'Blog',
    'Todo',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',
    'storages'
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

ROOT_URLCONF = 'Smart_blogging_system.urls'

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

WSGI_APPLICATION = 'Smart_blogging_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

LOGIN_URL = '/login/'

USE_S3 = True
# USE_S3 = ue

# implementation Ref
# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = "us-east-1"
    # AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    CLOUDFRONT_DISTRIBUTION_DOMAIN_NAME = config('CLOUDFRONT_DISTRIBUTION_DOMAIN_NAME', default=None)
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # implementation Ref for cloudfront cdn
    # https://appliku.com/post/django-file-uploads-s3-and-cloudfront-cdn/
    if CLOUDFRONT_DISTRIBUTION_DOMAIN_NAME:
        AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DISTRIBUTION_DOMAIN_NAME

    # s3 static settings
    AWS_LOCATION = 'staticfiles'
    STATIC_URL = f'{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'Smart_blogging_system.storage_backends.StaticStorage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'Smart_blogging_system.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# FROALA_UPLOAD_PATH = os.path.join(BASE_DIR,"media")
# FILE_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

#  https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
# we can customize more fields as per our requirement by going through above link

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD': 'id',
    "UPDATE_LAST_LOGIN": True,
}

AUTH_USER_MODEL = 'accounts.blogingUser'

AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']