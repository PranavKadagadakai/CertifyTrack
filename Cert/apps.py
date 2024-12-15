from django.apps import AppConfig


class CertConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cert'
    
    def ready(self):
        import Cert.signals  # Import the signals module
