import json
import logging

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from wagtail.models import Site

logger = logging.getLogger(__name__)


class SiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.site = Site.find_for_request(request)
        except Site.DoesNotExist:
            request.site = None
        return self.get_response(request)


class HtmxMessageMiddleware(MiddlewareMixin):
    def process_response(self, request: HttpRequest, response: HttpResponse):
        if "HX-Request" not in request.headers or 300 <= response.status_code < 400:
            return response

        messages = [
            {"message": str(message.message), "tags": message.tags}
            for message in get_messages(request)
        ]
        if not messages:
            return response

        try:
            hx_trigger = json.loads(response.headers.get("HX-Trigger", "{}"))
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in HX-Trigger header")
            hx_trigger = {}

        hx_trigger["messages"] = messages
        response.headers["HX-Trigger"] = json.dumps(hx_trigger)

        return response
