from django import template
from wagtail.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    if "request" not in context:
        return None
    return Site.find_for_request(context["request"]).root_page



def get_locations(self):
    for block in self.location:
        print("block*************",block)
        if block.block_type == "locations":
            print("the value//////////",block.value)
            return block.value
    return []