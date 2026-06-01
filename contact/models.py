from django.db import models

# models.py
from django.utils import timezone
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel
from wagtail.blocks import EmailBlock, StreamBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from config.utils import HTMXFormMixin
from recruitment.models import CustomFormBuilder


class FormField(AbstractFormField):
    """Custom form field for contact form"""

    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactPage(HTMXFormMixin, AbstractEmailForm):
    """Page model for 'Contact' with integrated form"""

    hero_title = models.CharField(
        max_length=255, default="Contactez-Nous", verbose_name="Titre principal"
    )
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )

    hero_subtitle = models.CharField(
        max_length=500, blank=True, verbose_name="Sous-titre"
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    location = StreamField(
        [
            (
                "locations",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("label", blocks.CharBlock(required=True)),
                            ("address", blocks.CharBlock(required=True)),
                            ("google_maps_link", blocks.TextBlock(required=False)),
                            ("latitude", blocks.FloatBlock(required=False)),
                            ("longitude", blocks.FloatBlock(required=False)),
                        ]
                    )
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Locations",
    )

    phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")

    office_hours = models.CharField(
        max_length=255, blank=True, verbose_name="Horaires d'ouverture"
    )

    # Map
    map_embed_code = models.TextField(
        blank=True,
        verbose_name="Code d'intégration de la carte",
        help_text="Code iframe de Google Maps ou autre service de cartographie",
    )
    # --- Réseaux sociaux ---
    facebook_url = models.URLField("Facebook", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    youtube_url = models.URLField("YouTube", blank=True)
    twitter_url = models.URLField("Twitter", blank=True)

    recipients_emails = StreamField(
        StreamBlock(
            [
                ("email", EmailBlock()),
            ]
        ),
        blank=True,
        verbose_name="emails qui recevront les formulaires de contact et recrutement",
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("hero_title"),
        # FieldPanel("hero_subtitle"),
        FieldPanel("featured_image"),
        FieldPanel("location"),
        FieldPanel("facebook_url"),
        FieldPanel("instagram_url"),
        FieldPanel("linkedin_url"),
        FieldPanel("twitter_url"),
        FieldRowPanel(
            [
                FieldPanel("phone"),
                FieldPanel("email"),
            ]
        ),
        # FieldPanel("office_hours"),
        FieldPanel("map_embed_code"),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FormSubmissionsPanel(),
        FieldPanel("recipients_emails"),
    ]

    class Meta:
        verbose_name = "Page Contact"

    subpage_types = []
    form_builder = CustomFormBuilder

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        for name, field in form.fields.items():
            # Only for inputs / textareas
            if hasattr(field.widget, "attrs"):
                field.widget.attrs.setdefault("placeholder", field.label)

        return form

    def get_recipient_list(self):
        return [block.value for block in self.recipients_emails or []]


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    panels = [
        FieldPanel("email"),
        FieldPanel("created_at"),
    ]

    def __str__(self):
        return self.email

    # @property
    # def base_form_class(self):
    #     from contact.forms import NewsletterSubscriptionForm
    #     return NewsletterSubscriptionForm

    base_form_class = "contact.forms.NewsletterSubscriptionForm"

    class Meta:
        verbose_name = "Newsletter subscriber"
        verbose_name_plural = "Newsletter subscribers"


# Define a ViewSet to control the menu placement
class NewsletterViewSet(SnippetViewSet):
    model = NewsletterSubscription
    icon = "mail"
    menu_label = "Newsletter"
    menu_name = "newsletter"
    menu_parent = "forms"  # This attempts to nest it under the Forms menu
    add_to_admin_menu = True  # This adds it to the main sidebar
    menu_order = 300  # Adjust this to place it near 'Forms'
    list_export = ("email", "created_at")
    # Optional: Customize the export filename
    export_filename = "Newsletter Abonnés"
    # Optional: Customize the column headings in the export file
    export_headings = {
        "created_at": "inscrit le",
    }

    def get_form_class(self, for_update=False):
        from contact.forms import NewsletterSubscriptionForm

        return NewsletterSubscriptionForm


# Register the ViewSet instead of the model directly
register_snippet(NewsletterViewSet)


class FqaServicesProvided(models.Model):
    faq = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            (
                                "service",
                                blocks.CharBlock(required=True, label="service"),
                            ),
                            (
                                "detail",
                                blocks.RichTextBlock(required=True, label="detail"),
                            ),
                        ]
                    )
                ),
            )
        ],
        blank=True,
        use_json_field=True,
    )
    faq.verbose_name = "The services provided by Maioreb are:"

    panels = [
        FieldPanel("faq"),
    ]

    class Meta:
        verbose_name = "The services provided by Maioreb are:"
        verbose_name_plural = "The services provided by Maioreb are:"


register_snippet(FqaServicesProvided)
