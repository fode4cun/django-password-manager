import socket
from ._base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-3] + "0.1" for ip in ips]

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

# django-debug-toolbar
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

# Postgres backend
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str("DATABASE_NAME"),
        'USER': env.str("DATABASE_USER"),
        'PASSWORD': env.str("DATABASE_PASSWORD"),
        'HOST': env.str("DATABASE_HOST"),
        'PORT': env.str("DATABASE_PORT"),
    }
}

# Logging with python rich package
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"rich": {"datefmt": "[%X]"}},
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
        }
    },
    "loggers": {"django": {"handlers": ["console"]}},
}
