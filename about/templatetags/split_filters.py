from django import template

register = template.Library()

@register.filter
def split(value, sep=','):
    if value is None:
        return []
    return [s.strip() for s in str(value).split(sep)]