# apps/mods/apps.py
from django.apps import AppConfig

class ModsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mods"
    verbose_name = "Mods"