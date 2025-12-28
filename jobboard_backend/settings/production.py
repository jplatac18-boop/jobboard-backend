# jobboard_backend/settings/production.py
from .base import *
import os

DEBUG = False

# Opción 1: Leer desde entorno (Render)
#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Si prefieres fijarlo aquí directamente, usa en lugar de lo anterior:
ALLOWED_HOSTS = [
    "jobboard-backend-g8kv.onrender.com",
    "localhost",
    "127.0.0.1",
]

# Indicar a Django que confíe en el proxy de Render para HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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
