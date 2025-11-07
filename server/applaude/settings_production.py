# server/applaude/settings_production.py

import os
from .settings import * # Import all base settings

# General Production Overrides
DEBUG = False # MUST be False in production
SECRET_KEY = config('SECRET_KEY') 
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=lambda v: [s.strip() for s in v.split(',')])

# --- Security & HTTPS Settings (Crucial for SaaS deployment) ---
# Enforce security for all cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Redirect all HTTP traffic to HTTPS
SECURE_SSL_REDIRECT = True
# Enable HTTP Strict Transport Security (HSTS) for 1 year
SECURE_HSTS_SECONDS = 31536000 
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Trust the proxy header from Digital Ocean/load balancer
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- CORS & Host Control ---
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default=[], cast=lambda v: [s.strip() for s in v.split(',')])

# --- Static Files & Deployment ---
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Use the default static file storage for production
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage' 

# --- Logging (Critical for debugging production server issues) ---
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
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
