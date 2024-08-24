from pathlib import Path
from settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = settings.SECRET_KEY.get_secret_value()
DEBUG = settings.DEBUG
ALLOWED_HOSTS = settings.ALLOWED_HOSTS.split(' ')

# BASE
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'catalog',
]

# PACKAGES
INSTALLED_APPS += [
    'imagekit',
    'tinymce',
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
        'DIRS': [Path(BASE_DIR, 'catalog/templates/catalog')],
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

DATABASES = {
    'default': {
        'ENGINE': settings.ENGINE,
        'NAME': settings.NAME_DB,
        'USER': settings.USER,
        'PASSWORD': settings.PASSWORD,
        'HOST': settings.HOST,
        'PORT': settings.PORT,
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

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

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC AND MEDIA
STATIC_URL = 'static/'
STATICFILES_DIRS = [Path(BASE_DIR, "static")]

MEDIA_URL = "media/"
MEDIA_ROOT = Path(BASE_DIR, "media")

PDF_DIR = Path(MEDIA_ROOT, "pdf")
FONT_DIR = Path(BASE_DIR, 'static', 'fonts')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = settings.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = settings.CELERY_RESULT_BACKEND
