from .base import *
import os


print("Django dev settings loaded successfully")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Adjust the level as needed
    },
}



# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Media and Static files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "../", "mediafiles")
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "../", "staticfiles")