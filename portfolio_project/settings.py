import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-portfolio-secret-key-replace-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*', '.onrender.com', 'saiwith.tech', 'www.saiwith.tech', 'home.saiwith.tech']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps',
    'blog',
    'projects',
]

MIDDLEWARE = [
    'portfolio_project.middleware.DomainRedirectMiddleware',  # Add redirect middleware first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'

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

WSGI_APPLICATION = 'portfolio_project.wsgi.application'

# Database Configuration
import os

# Database Configuration
# Use SQLite for development, Azure SQL for production
if os.environ.get('USE_AZURE_SQL') == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': os.environ.get('DB_NAME', 'portfolio'),
            'USER': os.environ.get('DB_USER', 'mysterious3115_gmail.com#EXT#@mysterious3115gmail.onmicrosoft.com'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'portfoli.database.windows.net'),
            'PORT': os.environ.get('DB_PORT', '1433'),
            'OPTIONS': {
                'driver': 'ODBC Driver 18 for SQL Server',
                'extra_params': 'Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=60;Login Timeout=60;Authentication=ActiveDirectoryPassword;'
            },
        }
    }
else:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
