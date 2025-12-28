from .base import *
import os

DEBUG = False

# Leer desde variable de entorno en Render
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# 1) HSTS (solo si TODO el tráfico va por HTTPS)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 2) Redirigir todo a HTTPS
SECURE_SSL_REDIRECT = True

# 3) Cookies solo por HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Evitar que tu sitio se embeba en iframes (clickjacking)
X_FRAME_OPTIONS = "DENY"

# Evitar que el navegador adivine tipos de contenido
SECURE_CONTENT_TYPE_NOSNIFF = True

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")
