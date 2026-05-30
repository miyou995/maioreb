from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page


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
        max_length=255, default="Nos Missions", verbose_name="Titre de la mission"
    )

    mission_content = RichTextField(blank=True, verbose_name="Contenu de la mission")

    vision_title = models.CharField(
        max_length=255, default="Nos Vision", verbose_name="Titre de la vision"
    )

    vision_content = RichTextField(blank=True, verbose_name="Contenu de la vision")

    values_title = models.CharField(
        max_length=255, default="Nos Valeurs", verbose_name="Titre des valeurs"
    )

    values = StreamField(
        [
            (
                "values_items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("title", blocks.TextBlock(required=True, label="titre")),
                            (
                                "description",
                                blocks.RichTextBlock(
                                    required=True, label="Description"
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
    values.verbose_name = "valeurs"

    timeline = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("year", blocks.CharBlock(required=True, label="année")),
                            (
                                "event",
                                blocks.TextBlock(required=True, label="événement"),
                            ),
                            (
                                "description",
                                blocks.RichTextBlock(
                                    required=True, label="Description"
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
    timeline.verbose_name = "histoire"

    key_numbers = StreamField(
        [
            (
                "numbers",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            (
                                "number",
                                blocks.CharBlock(required=True, label="chiffre"),
                            ),
                            ("label", blocks.CharBlock(required=True, label="label")),
                            (
                                "symbol",
                                blocks.CharBlock(required=False, label="symbole"),
                            ),
                        ]
                    )
                ),
            )
        ],
        blank=True,
        use_json_field=True,
    )
    key_numbers.verbose_name = "chiffres clés"

    leadership = StreamField(
        [
            (
                "members",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("photo", ImageChooserBlock(required=False, label="photo")),
                            ("name", blocks.CharBlock(required=True, label="nom")),
                            (
                                "position",
                                blocks.CharBlock(required=True, label="position"),
                            ),
                            # ('bio', blocks.TextBlock(required=True,label="bio")),
                        ]
                    )
                ),
            )
        ],
        blank=True,
        use_json_field=True,
    )
    leadership.verbose_name = "équipe dirigeante"

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        FieldPanel("mission_title"),
        FieldPanel("mission_content"),
        FieldPanel("vision_title"),
        FieldPanel("vision_content"),
        FieldPanel("values_title"),
        FieldPanel("values"),
        FieldPanel("timeline"),
        FieldPanel("key_numbers"),
        FieldPanel("leadership"),
    ]

    class Meta:
        verbose_name = "Page Qui sommes nous ?"

    parent_page_types = ["EntrepriseIndexPage"]
    subpage_types = []

    def get_context(self, request):
        from home.models import HomePage

        context = super().get_context(request)
        context["home_page"] = HomePage.objects.live().specific().first()
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
        max_length=255, default="Our Vision", verbose_name="Vision title"
    )
    vision_content = RichTextField(blank=True, verbose_name="Vision content")

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
        FieldPanel("mission_title"),
        FieldPanel("mission_content"),
    ]

    class Meta:
        verbose_name = "What We Do Page"

    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        return context

    @property
    def get_contact_page(self):
        return _contact_page()
