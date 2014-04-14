from django import template

register = template.Library()


@register.filter(name='get')
def get(d, key):
    return d.get(key, None)
