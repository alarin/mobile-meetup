# -*- coding: UTF-8 -*-
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = Library()

@register.filter(name='email_encode')
@stringfilter
def email_encode(value, addProto=1):
    """
    Encodes email by &#xxx; entities.

    If you specify ``"False"`` as a param to filter, it won't add "mailto:"
    in front of the email. Otherwise it will.

    """
    if addProto == 1:
        value = ''.join('mailto:%s' % value)
    return mark_safe(''.join('&#%d;' % ord(char) for char in value))
