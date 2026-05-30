from django.db import models
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class LegalPage(Page):
    """Page model for 'Mentions légales & RGPD' (Legal Notices & GDPR)"""

    hero_title = models.CharField(
        max_length=255,
        default="Mentions Légales & RGPD",
        verbose_name="Titre principal",
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("introduction"),
        FieldPanel("featured_image"),
    ]

    class Meta:
        verbose_name = "Page Mentions légales & RGPD"

    subpage_types = ["ItemLegalPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["items"] = self.get_children().live().specific()
        return context  


class ItemLegalPage(Page):
    subtitle = models.CharField(max_length=255, blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )
    summary = models.CharField(max_length=255, blank=True, verbose_name="Résumé")
    description = RichTextField(blank=True, verbose_name="Description détaillée")

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("summary"),
        FieldPanel("featured_image"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "notions des  mentions legales"

    subpage_types = []
    parent_page_types = ["LegalPage"]