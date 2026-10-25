from django.core.management.base import BaseCommand

from blog.models import BlogPost
from findBookCafe.models import Collection, Shop
from findBookCafe.thumbnails import ensure_thumbnails


class Command(BaseCommand):
    help = "Create missing WebP thumbnails for shop, collection and blog post images"

    def handle(self, *args, **options):
        names = set(Shop.objects.exclude(thumbnail='').values_list('thumbnail', flat=True))
        names |= set(Collection.objects.exclude(thumbnail='').values_list('thumbnail', flat=True))
        names |= set(BlogPost.objects.exclude(thumbnail='').values_list('thumbnail', flat=True))
        failed = 0
        for name in sorted(n for n in names if n):
            # Never block startup over one bad upload; pages fall back to the original image
            try:
                ensure_thumbnails(name)
            except Exception as error:
                failed += 1
                self.stderr.write(f"Skipped {name}: {error}")
        self.stdout.write(f"Thumbnails ready for {len(names) - failed} of {len(names)} images")
