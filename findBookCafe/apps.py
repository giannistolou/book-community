from django.apps import AppConfig


class FindbookcafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'findBookCafe'

    def ready(self):
        from . import signals  # noqa: F401
