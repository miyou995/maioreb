from django.apps import AppConfig


class ContactConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contact"


def ready(self):
    from wagtail.admin.forms.models import register_form_field_override  # noqa
