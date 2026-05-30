import os
from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import check_for_language
from django.views import View

# Create your views here.


class RobotsTxtView(View):
    """
    Serve the robots.txt file from static directory.
    """

    def get(self, request):
        robots_path = os.path.join(settings.BASE_DIR, "static", "robots.txt")
        try:
            with open(robots_path, "r") as f:
                content = f.read()
            return HttpResponse(content, content_type="text/plain")
        except FileNotFoundError:
            return HttpResponse("User-agent: *\nAllow: /", content_type="text/plain")


class MaintenanceView(View):
    """Render a simple maintenance page with 503 status."""

    def get(self, request):
        return render(request, "maintenance.html", status=503)


def _normalize_next_url(next_url):
    """Drop old locale prefixes (/fr/, /en/) from redirect targets."""
    if not next_url:
        return "/"

    path = urlsplit(next_url).path
    if not path.startswith("/"):
        path = f"/{path}"

    path_parts = [p for p in path.split("/") if p]
    supported_langs = {code for code, _ in settings.LANGUAGES}
    if path_parts and path_parts[0] in supported_langs:
        path_parts = path_parts[1:]
        path = "/" + "/".join(path_parts)
        if not path.endswith("/") and next_url.endswith("/"):
            path += "/"
        if path == "":
            path = "/"

    return path


def set_language(request, language=None):
    """Persist language in cookie for non-prefixed URL routing."""
    if request.method == "POST":
        language = request.POST.get("language")

    next_url = (
        request.POST.get("next")
        if request.method == "POST"
        else request.META.get("HTTP_REFERER")
    )
    if not next_url:
        next_url = "/"

    lang_code = (
        language
        if language and check_for_language(language)
        else settings.LANGUAGE_CODE
    )

    translation.activate(lang_code)
    request.LANGUAGE_CODE = lang_code

    response = HttpResponseRedirect(_normalize_next_url(next_url))
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response
