from wagtail.admin.forms.models import WagtailAdminModelForm

from .models import NewsletterSubscription


class NewsletterSubscriptionForm(WagtailAdminModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = [
            "email",
        ]
