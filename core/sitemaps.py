from django.contrib.sitemaps import Sitemap
from wagtail.models import Page


class WagtailPageSitemap(Sitemap):
    """
    Sitemap for all Wagtail pages.
    This will automatically include all live, public pages in your site.
    """

    changefreq = "weekly"
    priority = 0.5

    def items(self):
        # Get all live and public pages, excluding the root page
        return (
            Page.objects.live()
            .public()
            .filter(depth__gt=1)
            .order_by("-last_published_at")
        )

    def lastmod(self, obj):
        return obj.last_published_at

    def location(self, obj):
        return obj.get_url()

    def priority(self, obj):
        # Assign higher priority to top-level pages
        if obj.depth == 2:  # Direct children of root
            return 1.0
        elif obj.depth == 3:  # Second level
            return 0.8
        else:
            return 0.5
