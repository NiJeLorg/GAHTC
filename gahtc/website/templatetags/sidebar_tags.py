from django import template
from website.models import *

register = template.Library()

# sidebar snippets
@register.inclusion_tag('website/sidebar.html', takes_context=True)
def sidebarcontent(context):
    return {
        'sidebarcontent': sidebarContent.objects.all(),
        'request': context['request'],
    }