from django.apps import AppConfig


class LibraryConfig(AppConfig):
    name = 'library'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        """
        Import signals when the app is ready
        This ensures that signal handlers are registered
        """
        import library.signals  # noqa
