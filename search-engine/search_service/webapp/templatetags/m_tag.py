from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
@register.simple_tag(name='m_tag')
def m_tag(value):
    return str("{{{{{0}}}}}".format(value))# -*- coding: utf-8 -*-

