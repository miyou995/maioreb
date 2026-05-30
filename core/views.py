import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
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
