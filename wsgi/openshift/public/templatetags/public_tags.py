from django import template
register = template.Library()

from cms.utils.page_resolver import get_page_from_path
@register.inclusion_tag('public/frontpage_features.html', takes_context=True)
def get_features(context):
    context['root'] = get_page_from_path('ominaisuudet')
    context['features'] = context['root'].children.filter(published=True)
    for f in context['features']:
        setattr(f, 'plchld', {})
        for p in f.placeholders.all():
            f.plchld[p.slot] = p
    return context

@register.inclusion_tag('public/frontpage_slider.html', takes_context=True)
def get_slider(context):
    context['root'] = get_page_from_path('slider')
    context['slides'] = context['root'].children.filter(published=True)
    for s in context['slides']:
        setattr(s, 'plchld', {})
        for p in s.placeholders.all():
            if p.slot == 'background':
                setattr(s, 'background', p.get_plugins()[0].filerimage.image.url)
            s.plchld[p.slot] = p
    return context

@register.inclusion_tag('public/frontpage_testimonial.html', takes_context=True)
def random_testimonial(context):
    context['root'] = get_page_from_path('referenssit')
    context['testimonial'] = context['root'].children.filter(published=True).order_by('?')[0]
    for p in context['testimonial'].placeholders.all():
        context[p.slot] = p
    return context
