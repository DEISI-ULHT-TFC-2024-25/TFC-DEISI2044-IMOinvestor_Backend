import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  
django.setup()

from announcements.tasks import desativar_anuncios_expirados

if __name__ == "__main__":
    desativar_anuncios_expirados()
