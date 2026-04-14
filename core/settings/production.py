from .base import *

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

DEBUG = False

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": int(os.environ["DB_PORT"]),
    }
}
