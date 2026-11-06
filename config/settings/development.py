from .base import *

DEBUG = True

# Facilita desenvolvimento local
ALLOWED_HOSTS = ["*"]

# Debug Toolbar
INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ["127.0.0.1"]

# Emails no terminal
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Banco local pode usar sqlite para testes rápidos se preferir
# basta descomentar e comentar o DATABASES do base.py
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }