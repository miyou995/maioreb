from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from contact.models import ContactPage
from portfolio.models import PortfolioIndexPage


class ExpertiseIndexPage(Page):
    """Index page for 'Nos expertises' (Our Expertise)"""

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )

    introduction = RichTextField(blank=True, verbose_name="Introduction")

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("introduction"),
    ]
    subpage_types = ["ExpertisePage"]

    class Meta:
        verbose_name = "Page nos expertises"

    def get_context(self, request):
        context = super().get_context(request)
        # Get all child expertise pages
        context["expertises"] = self.get_children().live().specific()

        portfolio_page = PortfolioIndexPage.objects.live().specific().first()
        context["images"] = portfolio_page.images if portfolio_page else []

        return context

    def get_expertises(self):
        return self.get_children().live().specific()


class ExpertisePage(Page):
    """Individual expertise page"""

    subtitle = models.CharField(max_length=255, blank=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image principale",
    )
    summary = models.TextField(max_length=500, blank=True, verbose_name="petit text")

    description = RichTextField(blank=True, verbose_name="Description détaillée")

    services = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("title", blocks.CharBlock(label="Titre")),
                            ("description", blocks.RichTextBlock(label="Description")),
                        ]
                    )
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )
    services.verbose_name = "Nos domaines d’expertise & services"

    content = RichTextField(blank=True, verbose_name="Contenu")

    benifits = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("description", blocks.RichTextBlock(label="Description")),
                        ]
                    )
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )
    benifits.verbose_name = "Les bénéfices pour votre entreprise"

    passe_to_action = RichTextField(blank=True, verbose_name="Passer à l'action")
    faq = StreamField(
        [
            (
                "items",
                blocks.ListBlock(
                    blocks.StructBlock(
                        [
                            ("question", blocks.RichTextBlock(label="Question")),
                            ("answer", blocks.RichTextBlock(label="Réponse")),
                        ]
                    )
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )
    faq.verbose_name = "FAQ"

    content_panels = Page.content_panels + [
        FieldPanel("featured_image"),
        FieldPanel("summary"),
        FieldPanel("description"),
        FieldPanel("services"),
        FieldPanel("content"),
        FieldPanel("benifits"),
        FieldPanel("passe_to_action"),
        FieldPanel("faq"),
    ]

    class Meta:
        verbose_name = "Page Expertise"

    parent_page_types = ["expertise.ExpertiseIndexPage"]
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        parent = self.get_parent().specific
        context["expertises"] = parent.get_expertises()

        return context

    @property
    def get_contact_page(self):
        contact_page = ContactPage.objects.live().first()
        return contact_page if contact_page else None
