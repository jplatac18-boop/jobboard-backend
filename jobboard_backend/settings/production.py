# jobboard_backend/settings/production.py
from .base import *
import os

DEBUG = False

# ALLOWED_HOSTS desde entorno: "dominio1,dominio2"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Seguridad HTTP
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSP usando django-csp (coherente con base.py)
CSP_DEFAULT_SRC = ("'self'",)

CSP_SCRIPT_SRC = ("'self'",)

CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://fonts.googleapis.com",
)

CSP_IMG_SRC = (
    "'self'",
    "data:",
)

CSP_FONT_SRC = (
    "'self'",
    "https://fonts.gstatic.com",
)
