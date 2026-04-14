from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = []

DEBUG = True

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

