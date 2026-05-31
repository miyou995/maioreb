from django.core.paginator import Paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page

from about.models import AboutPage


class PortfolioIndexPage(Page):
    """Index page for 'Réalisations / Clients' (Portfolio/Clients)"""

    # hero_title = models.CharField(
    #     max_length=255, default="Nos Réalisations", verbose_name="Titre principal"
    # )

    # hero_subtitle = models.CharField(
    #     max_length=500, blank=True, verbose_name="Sous-titre"
    # )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    clients_title = models.CharField(
        max_length=255,
        default="Nos Clients",
        verbose_name="Titre de la section clients",
    )
    images = StreamField(
        [
            ("image", ImageChooserBlock(required=True, label="Logos clients")),
        ],
        blank=True,
        use_json_field=True,
    )

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )

    reviews_banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de la section reviews",
    )

    content_panels = Page.content_panels + [
        # FieldPanel("hero_title"),
        # FieldPanel("hero_subtitle"),
        FieldPanel("introduction"),
        FieldPanel("clients_title"),
        FieldPanel("hero_image"),
        FieldPanel("reviews_banner"),
        FieldPanel("images"),
        InlinePanel("client_opinion", label="témoignages clients"),
    ]

    class Meta:
        verbose_name = "Page Réalisations / Clients"

    subpage_types = ["PortfolioPage"]

    def get_context(self, request):
        context = super().get_context(request)

        projects_qs = self.get_children().live().specific()
        paginator = Paginator(projects_qs, 6)
        page_number = request.GET.get("page")
        context["projects"] = paginator.get_page(page_number)

        context["clients_opinions"] = self.client_opinion.all()

        # about_page = AboutPage.objects.live().public().specific().first()
        # context["key_numbers"] = about_page.key_numbers if about_page else []

        context["images"] = self.images

        return context


class ClientOpinion(Orderable):
    """Client logo for the portfolio index page"""

    page = ParentalKey(
        PortfolioIndexPage, on_delete=models.CASCADE, related_name="client_opinion"
    )
    client_name = models.CharField(max_length=255, verbose_name="client")
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo",
    )
    quote = RichTextField(blank=True, verbose_name="avis de client")
    author = models.CharField(blank=True, verbose_name="Poste")

    panels = [
        FieldPanel("client_name"),
        FieldPanel("logo"),
        FieldPanel("author"),
        FieldPanel("quote"),
    ]


class PortfolioPage(Page):
    """Individual portfolio/project page"""

    client_name = models.CharField(
        max_length=255, blank=True, verbose_name="Nom du project"
    )

    project_date = models.DateField(
        null=True, blank=True, verbose_name="Date du projet"
    )

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )

    summary = models.TextField(max_length=500, blank=True, verbose_name="Résumé")

    challenge = RichTextField(blank=True, verbose_name="Défi / Problématique")

    solution = RichTextField(blank=True, verbose_name="Solution apportée")

    results = RichTextField(blank=True, verbose_name="Résultats")

    technologies = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Technologies utilisées",
        help_text="Séparées par des virgules",
    )

    project_url = models.URLField(blank=True, verbose_name="URL du projet")

    # body = StreamField([
    #     ("text", blocks.RichTextBlock()),
    #     ("image", ImageChooserBlock()),
    #     ("list", blocks.ListBlock(blocks.CharBlock())),
    # ], use_json_field=True, blank=True)
    # body.verbose_name="les détails du projet"

    content_panels = Page.content_panels + [
        FieldPanel("client_name"),
        FieldPanel("project_date"),
        FieldPanel("featured_image"),
        FieldPanel("summary"),
        FieldPanel("challenge"),
        FieldPanel("solution"),
        FieldPanel("results"),
        # FieldPanel("technologies"),
        # InlinePanel("gallery_images", label="Galerie d'images"),
    ]

    class Meta:
        verbose_name = "Page cas d'étude"

    parent_page_types = ["portfolio.PortfolioIndexPage"]
    subpage_types = []


# class PortfolioGalleryImage(Orderable):
#     """Gallery images for portfolio pages"""

#     page = ParentalKey(
#         PortfolioPage, on_delete=models.CASCADE, related_name="gallery_images"
#     )

#     image = models.ForeignKey(
#         "wagtailimages.Image",
#         on_delete=models.CASCADE,
#         related_name="+",
#         verbose_name="Image",
#     )

#     caption = models.CharField(max_length=255, blank=True, verbose_name="Légende")

#     panels = [
#         FieldPanel("image"),
#         FieldPanel("caption"),
#     ]
