from .base import *

DEBUG = False

# Segurança HTTPS (Ative em produção com certificado SSL via .env)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT            = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SESSION_COOKIE_SECURE          = config("SESSION_COOKIE_SECURE", default=False, cast=bool)
CSRF_COOKIE_SECURE             = config("CSRF_COOKIE_SECURE", default=False, cast=bool)
SECURE_HSTS_SECONDS            = config("SECURE_HSTS_SECONDS", default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False, cast=bool)
SECURE_HSTS_PRELOAD            = config("SECURE_HSTS_PRELOAD", default=False, cast=bool)
SECURE_BROWSER_XSS_FILTER      = True
SECURE_CONTENT_TYPE_NOSNIFF    = True
X_FRAME_OPTIONS                = "DENY"

# Email real (configure via .env)
EMAIL_BACKEND  = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST     = config("EMAIL_HOST",     default="smtp.gmail.com")
EMAIL_PORT     = config("EMAIL_PORT",     default=587,  cast=int)
EMAIL_USE_TLS  = config("EMAIL_USE_TLS",  default=True, cast=bool)
EMAIL_HOST_USER     = config("EMAIL_HOST_USER",     default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
