from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel,InlinePanel
from wagtail.fields import RichTextField,StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel,MultiFieldPanel
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from modelcluster.tags import ClusterTaggableManager
from django.core.paginator import Paginator
from recruitment.models import RecruitmentIndexPage
from django.db.models import Q
from taggit.models import Tag



class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogIndexPage(Page):
    """Index page for Blog / Insights"""

    # hero_title = models.CharField(
    #     max_length=255, default="Blog & Insights", verbose_name="Titre principal"
    # )

    # hero_subtitle = models.CharField(
    #     max_length=500, blank=True, verbose_name="Sous-titre"
    # )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image d'en-tête",
    )

    intro = RichTextField(blank=True, verbose_name="Introduction")
    

    

    content_panels = Page.content_panels + [
        # FieldPanel("hero_title"),
        # FieldPanel("hero_subtitle"),
        FieldPanel("intro"),
        FieldPanel("hero_image"),
    ]



    class Meta:
        verbose_name = "Page du Blog / Insights"

    # subpage_types = ["blog.ArticlePage"]

    def get_context(self, request):
        context = super().get_context(request)

        tag = request.GET.get('tag')
        search = request.GET.get("search")

        # posts_qs = self.get_children().live().specific().order_by("-first_published_at")
        posts_qs = BlogPage.objects.live().public().order_by("-date")

        ## tag ####
        if tag:
            posts_qs = posts_qs.filter(tags__slug=tag)
        # SEARCH FILTER
        if search:
            posts_qs = posts_qs.filter(
                Q(title__icontains=search) |
                Q(subtitle__icontains=search) |
                Q(content__icontains=search)
            )

        ## PAGINATION ####
        paginator = Paginator(posts_qs, 4)
        page_number = request.GET.get('page')

        context["posts"] = paginator.get_page(page_number)
        context["selected_tag"] = tag
        context["search_query"] = search

        # ALL TAGS (for sidebar)
        context["all_tags"] = Tag.objects.filter(
        blog_blogpagetag_items__isnull=False
        ).distinct()

        #### GET COMPANY CULTURES
        # job_page = RecruitmentIndexPage.objects.live().specific().first()
        # context["cultures"] = job_page.culture if job_page else []
        return context
    
    subpage_types = ["BlogPage"]
    # parent_page_types = ['wagtailcore.Page']

#addeded vcomment 

class BlogPage(Page):
    tags = ClusterTaggableManager(through="blog.BlogPageTag", blank=True)
    subtitle = models.CharField(max_length=250, blank=True,verbose_name="titre")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image de couverture"
    )
    date = models.DateField('Date')
    author = models.CharField(max_length=255, blank=True,verbose_name="auteur")
    reading_time = models.IntegerField(blank=True, null=True, verbose_name="Temps de lecture")
    content = RichTextField(blank=True, verbose_name="Contenu")
   
    # body = StreamField(
    #     [
    #         ("paragraph", blocks.RichTextBlock()),
    #         ("image", ImageChooserBlock()),
    #         ("quote", blocks.BlockQuoteBlock()),
    #     ],
    #     use_json_field=True,
    #     blank=True,
    # )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("date"),
                FieldPanel("image"),
                FieldPanel("tags"),    
                FieldPanel("content"),
                FieldPanel("author"),
                FieldPanel("reading_time"),
            ],
            heading="Informations",
        ),
        # FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        blog_index = self.get_parent().specific

        context["blog_index"] = blog_index
        context["selected_tag"] = request.GET.get("tag")
        context["search_query"] = request.GET.get("search")

        context["all_tags"] = Tag.objects.filter(
            blog_blogpagetag_items__isnull=False
        ).distinct()

        return context

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []
