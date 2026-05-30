from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4=+*(^i_=tj8=0&#5079713*x4)880+l7p1rnx&_5tkxt_g3+0"
# SECURITY WARNING: define the correct hosts in production!

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "hello@octopus-consulting.com"
EMAIL_HOST = "mail.octopus-consulting.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "hello@octopus-consulting.com"
EMAIL_HOST_PASSWORD = "miyou0209"

# COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
# INSTALLED_APPS += [  # noqa
#     "debug_toolbar",
# ]

# MIDDLEWARE += [  # noqa
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
# ]
# INTERNAL_IPS = ("127.0.0.1",)


# LANGUAGE_CODE = "en"


# SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
