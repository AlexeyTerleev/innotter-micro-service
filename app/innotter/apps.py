from django.apps import AppConfig


class InnotterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "innotter"

    def ready(self):
        import innotter.signals
