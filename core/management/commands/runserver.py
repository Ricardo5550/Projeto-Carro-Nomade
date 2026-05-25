from django.conf import settings
from django_extensions.management.commands.runserver_plus import Command as Base
 
class Command(Base):
    def handle(self, *args, **options):
        if not options.get("cert_path"):
            options["cert_path"] = getattr(settings, "CERT_FILE", None)
        if not options.get("key_file_path"):
            options["key_file_path"] = getattr(settings, "KEY_FILE", None)
        super().handle(*args, **options)