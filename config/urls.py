from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from core.sitemaps import WagtailPageSitemap
from core.views import MaintenanceView, RobotsTxtView
from search import views as search_views

sitemaps = {
    "pages": WagtailPageSitemap,
}

urlpatterns = [
    path("", MaintenanceView.as_view(), name="maintenance"),
    path("", include("contact.urls")),
    path("django-admin/", admin.site.urls),
    path("maioreb-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"),
    path("", include(wagtail_urls)),
]


if settings.DEBUG:
    # import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # urlpatterns = [
    #     path("__debug__/", include(debug_toolbar.urls)),
    # ] + urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
