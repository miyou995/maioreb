from .base import *  # noqa

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage

LANGUAGE_CODE = "fr-fr"
CACHE_BACKEND = "django.core.cache.backends.redis.RedisCache"
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
WHITENOISE_MAX_AGE = 2600000

# Security Headers (Helps with the 'Security' score)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# ALLOWED_HOSTS = "atrisgroupe.com", "www.atrisgroupe.com"
