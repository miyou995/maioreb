# from django.db import models
# from modelcluster.fields import ParentalKey
# from modelcluster.models import ClusterableModel
# from wagtail.admin.panels import FieldPanel, StreamFieldPanel, MultiFieldPanel,FieldRowPanel
# from wagtail.fields import RichTextField, StreamField
# from wagtail import blocks
# from wagtail.images.blocks import ImageChooserBlock
# from wagtail.models import Page, Orderable
# from wagtail.snippets.models import register_snippet
# from wagtail.search import index




# class HeroBlock(blocks.StructBlock):
#     title = blocks.CharBlock()
#     subtitle = blocks.TextBlock(required=False)
#     image = ImageChooserBlock(required=False)
#     cta_text = blocks.CharBlock(required=False)
#     cta_link = blocks.URLBlock(required=False)


# class StatsBlock(blocks.StructBlock):
#     number = blocks.CharBlock()
#     label = blocks.CharBlock()


# class TestimonialBlock(blocks.StructBlock):
#     testimonial = blocks.PageChooserBlock(target_model='snippets.Testimonial')


# class TeamBlock(blocks.StructBlock):
#     member = blocks.PageChooserBlock(target_model='snippets.TeamMember')