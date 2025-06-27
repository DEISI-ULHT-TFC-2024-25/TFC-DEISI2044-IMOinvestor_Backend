from django.utils import timezone
from announcements.models import Announcement

def desativar_anuncios_expirados():
    anuncios = Announcement.objects.filter(active=True, expires_at__lt=timezone.now())
    for anuncio in anuncios:
        anuncio.active = False
        anuncio.save()
