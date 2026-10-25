import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import BlogPost

from .models import Collection, Shop
from .thumbnails import ensure_thumbnails

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Shop)
@receiver(post_save, sender=Collection)
@receiver(post_save, sender=BlogPost)
def create_thumbnails(sender, instance, **kwargs):
    # A failed thumbnail must never block saving in the admin; pages fall back to the original
    try:
        ensure_thumbnails(str(instance.thumbnail or ''))
    except Exception:
        logger.exception("Thumbnail generation failed for %s", instance.thumbnail)
