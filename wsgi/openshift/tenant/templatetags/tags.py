from django import template
register = template.Library()

from django.core.urlresolvers import reverse

@register.simple_tag
def active(request, pattern):
    if reverse(pattern) in request.path:
        return 'class="active"'
    return ''
