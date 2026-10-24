import io
import logging
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)

THUMBNAIL_WIDTHS = (400, 600, 800, 1200)
WEBP_QUALITY = 80


def thumbnail_name(name, width):
    return str(PurePosixPath('thumbs', str(width), name).with_suffix('.webp'))


def _is_fresh(source_name, target_name):
    if not default_storage.exists(target_name):
        return False
    return default_storage.get_modified_time(target_name) >= default_storage.get_modified_time(source_name)


def ensure_thumbnails(name):
    """Create WebP copies of an uploaded image and return {width: name}.

    Widths larger than the original are skipped so images are never upscaled.
    Returns an empty dict when the source cannot be read, so callers can fall
    back to the original file.
    """
    if not name or not default_storage.exists(name):
        return {}
    try:
        with default_storage.open(name) as source_file:
            source = ImageOps.exif_transpose(Image.open(source_file))
            source.load()
    except (OSError, ValueError):
        logger.warning("Cannot read image %s for thumbnails", name, exc_info=True)
        return {}

    thumbnails = {}
    for width in THUMBNAIL_WIDTHS:
        target_width = min(width, source.width)
        target_name = thumbnail_name(name, width)
        if not _is_fresh(name, target_name):
            _save_webp(source, target_width, target_name)
        thumbnails[target_width] = target_name
        if width >= source.width:
            break
    return thumbnails


def _save_webp(source, width, target_name):
    resized = source.copy()
    resized.thumbnail((width, width * 10), Image.Resampling.LANCZOS)
    if resized.mode not in ('RGB', 'RGBA'):
        resized = resized.convert('RGBA' if 'transparency' in resized.info else 'RGB')
    buffer = io.BytesIO()
    resized.save(buffer, 'WEBP', quality=WEBP_QUALITY, method=6)
    if default_storage.exists(target_name):
        default_storage.delete(target_name)
    default_storage.save(target_name, ContentFile(buffer.getvalue()))
