from django.urls import path

from .views import newsletter_subscribe

app_name = "contact"

urlpatterns = [
    path("newsletter/subscribe/", newsletter_subscribe, name="newsletter_subscribe"),
]
