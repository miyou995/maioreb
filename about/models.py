from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.documents.blocks import DocumentChooserBlock

from contact.models import FqaServicesProvided


def _contact_page():
    from contact.models import ContactPage

    return ContactPage.objects.live().first()


class AboutPage(Page):
    """Page model for 'Qui sommes-nous ?' (About Us)"""

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    mission_title = models.CharField(
        max_length=255, default="More details", verbose_name="More details"
    )

    mission_content = RichTextField(blank=True, verbose_name="content (More details)")
    mission_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="image of the content",
    )
    history = RichTextField(blank=True, verbose_name="history")


    # vision_title = models.CharField(
    #     max_length=255, default="Nos Vision", verbose_name="Titre de la vision"
    # )

    # vision_content = RichTextField(blank=True, verbose_name="Contenu de la vision")

    values_title = models.CharField(
        max_length=255, default="Nos Valeurs", verbose_name="Titre des valeurs"
    )

    images = StreamField(
        [
            ("image", ImageChooserBlock(required=True, label="about us images")),
        ],
        blank=True,
        use_json_field=True,
    )
    client_logo = StreamField(
        [
            ("image", ImageChooserBlock(required=True, label="our client logos")),
        ],
        blank=True,
        use_json_field=True,
    )
    certified = StreamField(
        [
        (
            "items",
            blocks.ListBlock(
                blocks.StructBlock(
                    [
                        ("label", blocks.CharBlock(required=True, label="Label")),
                        (
                            "document",
                            DocumentChooserBlock(
                                required=True,
                                label="Document",
                            ),
                        ),
                    ]
                )
            ),
        )
    ],
        blank=True,
        use_json_field=True,
    )
    certified.verbose_name = "Maioreb certified"

    
    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        FieldPanel("images"),
        # FieldPanel("mission_title"),
        FieldPanel("mission_content"),
        FieldPanel("mission_image"),
        FieldPanel("client_logo"),
        FieldPanel("history"),
        FieldPanel("certified"),
   
    ]

    class Meta:
        verbose_name = "About us"

    # parent_page_types = ["EntrepriseIndexPage"]
    # subpage_types = []

    def get_context(self, request):
        from home.models import HomePage

        context = super().get_context(request)
        context["home_page"] = HomePage.objects.live().specific().first()
        context["what_we_do_page"] = WhatWeDoPage.objects.live().specific().first()
        context["faq_data"] = FqaServicesProvided.objects.all()
        
        return context

    @property
    def get_contact_page(self):
        return _contact_page()


class EntrepriseIndexPage(Page):
    not_clicable = models.BooleanField(default=True, verbose_name="Non cliquable")

    promote_panels = Page.promote_panels + [
        FieldPanel("not_clicable"),
    ]
    subpage_types = ["AboutPage"]
    max_count = 1

    class Meta:
        verbose_name = "Entreprise"


class WhatWeDoPage(Page):
    """Single 'What We Do' page replacing the old expertise index+detail pattern."""

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero image",
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    services = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            (
                                "icon",
                                blocks.CharBlock(
                                    required=False,
                                    label="Material Symbols icon name (e.g. analytics)",
                                ),
                            ),
                            ("title", blocks.CharBlock(label="Title")),
                            (
                                "description",
                                blocks.RichTextBlock(
                                    required=False, label="Description"
                                ),
                            ),
                        ]
                    )
                ),
            )
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Services",
    )

    vision_title = models.CharField(
        max_length=255, default="Vision & Mission", verbose_name="Vision & Mission title"
    )
    vision_content = RichTextField(blank=True, verbose_name="Vision & Mission content")

    mission_title = models.CharField(
        max_length=255, default="Our Mission", verbose_name="Mission title"
    )
    mission_content = RichTextField(blank=True, verbose_name="Mission content")

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        FieldPanel("services"),
        FieldPanel("vision_title"),
        FieldPanel("vision_content"),
        # FieldPanel("mission_title"),
        # FieldPanel("mission_content"),
    ]

    class Meta:
        verbose_name = "What We Do Page"

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        context["faq_data"] = FqaServicesProvided.objects.all()
        print("context['faq_data']------------------------->>>", context["faq_data"])

        return context

    @property
    def get_contact_page(self):
        return _contact_page()
