from .base import *


print("Django prod settings loaded successfully")
# Email
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "'smtp.gmail.com'"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = config("EMAIL_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
# EMAIL_USE_TLS = True

# Redis Cache

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_BACKEND"),
    },
}

