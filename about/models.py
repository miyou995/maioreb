from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from contact.models import ContactPage


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

    parent_page_types = ['EntrepriseIndexPage']
    subpage_types = []


    def get_context(self, request):
        from home.models import HomePage

        context = super().get_context(request)

        context["rse_page"] = RsePage.objects.live().specific().first()
        context["home_page"] = HomePage.objects.live().specific().first()
        return context


class RsePage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )
    summary = models.TextField(max_length=500, blank=True, verbose_name="Résumé( sera affiché dans la page 'Qui sommes-nous ?' dans la section RSE)")
    description = RichTextField(blank=True, verbose_name="Contenu de RSE")

    award_section = RichTextField(blank=True, verbose_name="Contenu médaille")

    images = StreamField(
        [
            ("image", ImageChooserBlock(required=True, label="image médaille")),
        ],
        blank=True,
        use_json_field=True,
    )
    values = StreamField(
        [(
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
                    ])),)],
        blank=True,
        use_json_field=True,
    )
    values.verbose_name = "Nos piliers RSE"

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
    
    document_rse = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Document RSE",
    )
    date_document = models.DateField(null=True, blank=True, verbose_name="Dernière mise à jour")

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("summary"),
        FieldPanel("description"),
        FieldPanel("values"),
        FieldPanel("award_section"),
        FieldPanel("images"),
        FieldPanel("key_numbers"),
        FieldPanel("document_rse"),
        FieldPanel("date_document"),
    ]

    class Meta:
        verbose_name = "Page RSE"

    subpage_types = []
    parent_page_types = ['EntrepriseIndexPage']


    def get_context(self, request):
        context = super().get_context(request)
        return context

    @property
    def first_image(self):
        if self.images:
            for block in self.images:
                if block.block_type == "image":
                    return block.value
        return None
    
    @property
    def get_contact_page(self):
        contact_page = ContactPage.objects.live().first()
        return contact_page if contact_page else None


class EntrepriseIndexPage(Page):
    not_clicable = models.BooleanField(default=True, verbose_name="Non cliquable")

    promote_panels = Page.promote_panels + [
        FieldPanel("not_clicable"),
    ]
    subpage_types = ["AboutPage","RsePage"]  
    max_count = 2 

    class Meta:
        verbose_name = "Entreprise"
