from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from core.sitemaps import WagtailPageSitemap
from core.views import MaintenanceView, RobotsTxtView, set_language
from search import views as search_views

sitemaps = {
    "pages": WagtailPageSitemap,
}

urlpatterns = [
    path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"),
    path("set-language/", set_language, name="set_language"),
    path("set-language/<str:language>/", set_language, name="set_language_code"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("maintenance/", MaintenanceView.as_view(), name="maintenance"),
    path("django-admin/", admin.site.urls),
    path("maioreb-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("", include("contact.urls")),
    path("", include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
