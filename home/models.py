from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from about.models import AboutPage, WhatWeDoPage
from contact.models import ContactPage
from legal.models import LegalPage
from portfolio.models import PortfolioIndexPage


class HeroSlideBlock(blocks.StructBlock):
    background_image = ImageChooserBlock(
        required=True, help_text="Image de fond du slide"
    )
    # hero_title = blocks.CharBlock(
    #     required=True, max_length=255, help_text="Titre principal"
    # )
    # hero_subtitle = blocks.TextBlock(required=False, help_text="Sous-titre du slide")
    # hero_cta_text = blocks.CharBlock(
    #     required=False, max_length=50, default="Entrer dans l’univers ATR-IS"
    # )
    # cta_linked_page = blocks.PageChooserBlock(
    #     required=False, help_text="Lien du bouton CTA"
    # )

    class Meta:
        icon = "image"
        label = "Hero Slide"


class HomePage(Page):
    """Enhanced homepage with hero section and features"""

    # Hero Section
    hero_title = models.CharField(
        max_length=255,
        default="Nous sommes ATR-IS.",
        verbose_name="Titre principal(ce titre afficher dans hero section et déroule sur le ruban dans page d'accueil)",
    )
    hero_title_2 = models.CharField(
        max_length=255,
        default="Nous sommes ATR-IS.",
        verbose_name="Titre secondaire(ce titre afficher dans hero section apres le titre principal)",
    )

    hero_subtitle = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="petite introduction dans la section hero",
    )
    slides = StreamField(
        [("slide", HeroSlideBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Slides du hero",
    )

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="logo",
    )
    negative_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="logo negatif sur fond sombre",
    )

    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="favicon",
    )
    video = models.URLField(blank=True, verbose_name="Vidéo (YouTube/Vimeo)")

    hero_cta_text = models.CharField(
        max_length=50,
        default="what we do",
        verbose_name="Texte du bouton CTA",
    )

    cta_linked_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Lien du bouton CTA",
        related_name="+",  # Use '+' to avoid reverse accessor clashes
    )

    introduction = RichTextField(
        blank=True,
        verbose_name="Introduction",
    )

    home_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de la première section de la page d'accueil",
    )
    # posts_linkedin = StreamField(
    #     [
    #         (
    #             "items",
    #             blocks.ListBlock(
    #                 blocks.StructBlock(
    #                     [
    #                         ("image", ImageChooserBlock()),
    #                         ("introduction", blocks.RichTextBlock()),
    #                         ("link", blocks.URLBlock()),
    #                         ("date", blocks.DateBlock()),
    #                     ]
    #                 )
    #             ),
    #         )
    #     ],
    #     use_json_field=True,
    #     blank=True,
    # )
    # posts_linkedin.verbose_name = "Posts LinkedIn"

    sectors = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("image", ImageChooserBlock()),
                            ("title", blocks.CharBlock()),
                        ]
                    )
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_title_2"),
        FieldPanel("hero_subtitle"),
        FieldPanel("favicon"),
        FieldPanel("logo"),
        FieldPanel("negative_logo"),
        FieldPanel("home_image"),
        FieldPanel("slides"),
        FieldPanel("hero_cta_text"),
        FieldPanel("cta_linked_page"),
        # FieldPanel("sectors"),
    ]

    class Meta:
        verbose_name = "Page d'Accueil"

    @classmethod
    def can_create_at(cls, parent):
        # Only one HomePage allowed, under the root page (wagtailcore.Page)
        return super().can_create_at(parent) and not cls.objects.exists()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        ######### what we do #########
        what_we_do = WhatWeDoPage.objects.live().first()
        context["what_we_do"] = what_we_do

        ######### realisation #########
        portfolio = PortfolioIndexPage.objects.live().first()
        context["portfolio"] = portfolio
        context["projects"] = (
            portfolio.get_children()
            .live()
            .public()
            .specific()
            .order_by("-first_published_at")[:6]
            if portfolio
            else []
        )

        ######## recrutement ########
        # recruitment_index = RecruitmentIndexPage.objects.live().public().first()
        # context["recruitment_index"] = recruitment_index

        ######### chiffre cles
        about_page = AboutPage.objects.live().public().specific().first()
        context["about_page"] = about_page
        # ########## recrutement ##########
        # recrutement_index = RecruitmentIndexPage.objects.live().first()
        # context["recrutement_index"] = recrutement_index

        return context

    @property
    def get_what_we_do_page(self):
        return WhatWeDoPage.objects.live().first()

    @property
    def get_legal_url(self):
        legal_page = LegalPage.objects.live().first()
        return legal_page.get_url() if legal_page else None

    @property
    def get_contact_page(self):
        contact_page = ContactPage.objects.live().first()
        return contact_page if contact_page else None

    @property
    def get_culture_page(self):
        culture_page = CulturePage.objects.live().first()
        return culture_page if culture_page else None

    @property
    def get_about_page(self):
        about_page = AboutPage.objects.live().first()
        return about_page if about_page else None


class CultureBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre")
    text = blocks.RichTextBlock(label="Texte")
    image = ImageChooserBlock(label="Image", required=False)

    class Meta:
        icon = "pick"
        label = "Culture Block"


class CulturePage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )
    introduction = RichTextField(blank=True)
    culture_content = StreamField(
        [("element", CultureBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Ambiance / Culture interne",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
        FieldPanel("culture_content"),
    ]

    class Meta:
        verbose_name = "Page culture et ambiance"

    subpage_types = []  # No subpages needed
    # parent_page_types = ["home.HomePage"]

    # def get_context(self, request, *args, **kwargs):
    #     context = super().get_context(request, *args, **kwargs)
    #     # Get the culture page (assuming only one exists)
    #     context['culture_page'] = CulturePage.objects.live().first()
    #     return context


@register_setting
class CookieConsentSettings(BaseSiteSetting):
    enabled = models.BooleanField(default=True)

    message = models.TextField(default="We use cookies to improve your experience.")

    privacy_page = models.ForeignKey(
        Page, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("enabled"),
        FieldPanel("message"),
        FieldPanel("privacy_page"),
    ]

    class Meta:
        verbose_name = "Cookie Consent"
