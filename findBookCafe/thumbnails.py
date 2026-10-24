import io
import logging
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

THUMBNAIL_WIDTHS = (400, 600, 800, 1200)
WEBP_QUALITY = 80
# EXIF orientations that rotate the image by 90 degrees, swapping width and height
ROTATED_ORIENTATIONS = {5, 6, 7, 8}


def thumbnail_name(name, width):
    return str(PurePosixPath('thumbs', str(width), name).with_suffix('.webp'))


def _is_fresh(source_name, target_name):
    if not default_storage.exists(target_name):
        return False
    return default_storage.get_modified_time(target_name) >= default_storage.get_modified_time(source_name)


def _planned_thumbnails(name, source_width):
    """{actual width: thumbnail name} for every size, never upscaling the source."""
    planned = {}
    for width in THUMBNAIL_WIDTHS:
        planned[min(width, source_width)] = thumbnail_name(name, width)
        if width >= source_width:
            break
    return planned


def _source_width(image):
    if image.getexif().get(0x0112) in ROTATED_ORIENTATIONS:
        return image.height
    return image.width


def existing_thumbnails(name):
    """Thumbnails already on disk as {width: name}; cheap enough to call while rendering.

    Only reads the image header and never creates files, so a page never waits
    on image processing. Missing or stale thumbnails are left out and the
    caller falls back to the original image.
    """
    if not name or not default_storage.exists(name):
        return {}
    try:
        with default_storage.open(name) as source_file:
            width = _source_width(Image.open(source_file))
    except (OSError, ValueError):
        return {}
    return {
        thumb_width: thumb_name
        for thumb_width, thumb_name in _planned_thumbnails(name, width).items()
        if _is_fresh(name, thumb_name)
    }


def ensure_thumbnails(name):
    """Create any missing WebP copies of an uploaded image."""
    if not name or not default_storage.exists(name):
        return
    try:
        with default_storage.open(name) as source_file:
            source = ImageOps.exif_transpose(Image.open(source_file))
            source.load()
    except (OSError, ValueError):
        logger.warning("Cannot read image %s for thumbnails", name, exc_info=True)
        return

    for width, target_name in _planned_thumbnails(name, source.width).items():
        if not _is_fresh(name, target_name):
            _save_webp(source, width, target_name)


def _save_webp(source, width, target_name):
    resized = source.copy()
    resized.thumbnail((width, width * 10), Image.Resampling.LANCZOS)
    if resized.mode not in ('RGB', 'RGBA'):
        resized = resized.convert('RGBA' if 'transparency' in resized.info else 'RGB')
    buffer = io.BytesIO()
    resized.save(buffer, 'WEBP', quality=WEBP_QUALITY)
    if default_storage.exists(target_name):
        default_storage.delete(target_name)
    default_storage.save(target_name, ContentFile(buffer.getvalue()))
