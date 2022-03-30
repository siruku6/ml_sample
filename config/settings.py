"""
Django settings for ml_sample project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ENVIRONMENT=(str, None)
)
env_file = str(BASE_DIR.joinpath('.env'))
env.read_env(env_file)
VIRTUAL_ENVIRONMENT = env('ENVIRONMENT')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

####################
# SECURITY WARNING: keep the secret key used in production secret!
####################
SECRET_KEY = env('SECRET_KEY')
# DEBUG = env('DEBUG', False)
DEBUG = True  # MEDIA_URLを有効化するための暫定的措置
ALLOWED_HOSTS = ['*']

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'
LOGOUT_REDIRECT_URL = '/ml/login'

###########################################
#  Application definition (Core settings)
###########################################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mlapp',
    'classify_images',
    'detect_expression',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


###########################
#        Database
###########################
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
if VIRTUAL_ENVIRONMENT == 'heroku':
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES = {
        'default': db_from_env
    }
elif VIRTUAL_ENVIRONMENT == 'docker':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': 'postgres',
            'PORT': 5432,
            'TEST': {
                'NAME': 'life_record_test',
            },
        }
    }
# NOTE: reach this branch when running test or mypy
else:
    DATABASES = {}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


#################################
#     Internationalization
#################################
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


######################################################
#      Static files (CSS, JavaScript, Images)
######################################################
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

# NOTE: DEBUG = False だと動かんよ
# https://sinyblog.com/django/media_file_001/#DEBUGFalse
# https://rurukblog.com/post/Django-debug-false/
# https://jpcodeqa.com/q/4d05199e064cb6b60d1cc61fdc239ce0
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# heroku settings
import django_heroku
django_heroku.settings(locals())


###########################
#         Logging
###########################
LOGGING = {
    'version': 1,
    # Don't disable logger settings already exist
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d %(message)s '
                      '%(pathname)s:%(lineno)d',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'console': {
            'format': '%(asctime)s [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/app.log',
            'maxBytes': 50000,
            'backupCount': 3,
            'formatter': 'default',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
