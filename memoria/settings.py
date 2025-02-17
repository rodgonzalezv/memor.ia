from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xzvpr#7h@wk*-ldpx@lzt6^x=omvhq%8(tweeu))e+#)42wk!k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.memor-ia.cl', 'memor-ia.cl', '200.29.217.86','*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.core.mail',
    'mathfilters',
    'django.contrib.humanize',
    'web',
    'dashboard',
    'crispy_forms',
    'crispy_bootstrap4',
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

ROOT_URLCONF = 'memoria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'memoria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'memoria',
        'USER': 'memoria',
        'PASSWORD': 'memoria',
        'HOST': 'localhost',  # 'localhost' indica que la base de datos está en el mismo servidor
        'PORT': '5432',       # el puerto por defecto de PostgreSQL
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

BASE_DIR = Path(__file__).resolve().parent.parent

STATICFILES_DIRS = [
    BASE_DIR / "static",
    os.path.join(BASE_DIR, "static"),
    '/home/memoria/memoria/static',
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Servidor SMTP de Google
EMAIL_PORT = 465  # Puerto del servidor SMTP de Google

EMAIL_HOST_USER = 'memoria@virtual.cl'  # Dirección de correo electrónico de la cuenta de Google Workspace
EMAIL_HOST_PASSWORD = 'Django#DuocUC'  # Contraseña de la cuenta de Google Workspace
EMAIL_USE_SSL = True 