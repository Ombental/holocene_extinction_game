"""
Django settings for holocene_extinction_game project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.Value('ncYIiLiNBzZAbkximBPOmxnpxfouYlipaINXJAJVfNFUPlYfiL')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = values.ListValue([])  # Would be passed from above in the ecs task
    CORS_ALLOWED_ORIGINS = values.ListValue([])
    # Application definition
    THIRD_PARTY_APPS = [
        'corsheaders',
        'rest_framework_simplejwt',
        'rest_framework',
        'django_extensions',
        'import_export',
        'drf_spectacular'
    ]
    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    HOLOCENE_EXTINCTION_GAME_APPS = ["fauna"]
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + HOLOCENE_EXTINCTION_GAME_APPS

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'holocene_extinction_game.middleware.TimezoneMiddleware',
        'querycount.middleware.QueryCountMiddleware'

    ]
    QUERYCOUNT = {
        'THRESHOLDS': {
            'MEDIUM': 50,
            'HIGH': 200,
            'MIN_TIME_TO_LOG': 0,
            'MIN_QUERY_COUNT_TO_LOG': 5
        },
        'IGNORE_REQUEST_PATTERNS': [],
        'IGNORE_SQL_PATTERNS': [],
        'DISPLAY_DUPLICATES': None,
        'RESPONSE_HEADER': None
    }

    ROOT_URLCONF = 'holocene_extinction_game.urls'

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

    WSGI_APPLICATION = 'holocene_extinction_game.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/3.1/ref/settings/#databases

    # DATABASES = values.DatabaseURLValue('postgresql://holocene_extinction_game_user:holocene_extinction_game_pass@127.0.0.1:5432/holocene_extinction_game_db')
    DATABASES = values.DatabaseURLValue('sqlite:///holocene_extinction_game.db')

    # Password validation
    # https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
    # ACCEPTED_PERIOD = "PERMIAN"

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

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer'
        ),
        'PAGE_SIZE': 30
    }

    SIMPLE_JWT = {
        # Consider customizing other stuff here: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
        "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=30)
    }

    # Internationalization
    # https://docs.djangoproject.com/en/3.1/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    USER_TZ = values.Value()

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.1/howto/static-files/
    STATIC_ROOT = BASE_DIR / 'static'
    STATIC_URL = '/static/'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_ROOT = values.Value(BASE_DIR / 'media')
    MEDIA_URL = '/media/'


class Development(Base):
    CORS_ALLOW_ALL_ORIGINS = True
    ALLOWED_HOSTS = values.ListValue(["web", "localhost", "127.0.0.1"])

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


class Staging(Base):
    DEBUG = False
    CORS_ALLOW_ALL_ORIGINS = False
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_name="S3_STORAGE")


class Production(Base):
    DEBUG = False
    CORS_ALLOW_ALL_ORIGINS = False
    AWS_STORAGE_BUCKET_NAME = values.Value(environ_name="S3_STORAGE")
