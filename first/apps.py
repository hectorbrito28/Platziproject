"""App config"""

from django.apps import AppConfig


class FirstConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'first'
    verbose_name = "First"
