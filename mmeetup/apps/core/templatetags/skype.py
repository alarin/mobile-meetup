# -*- coding: UTF-8 -*-
import urllib

from django.template import Library
from django.utils.safestring import mark_safe


register = Library()

SKYPE_WIDGET_TEMPLATE = """
<script type="text/javascript" src="http://download.skype.com/share/skypebuttons/js/skypeCheck.js"></script>
<a href="skype:%s?call">
    <img src="http://mystatus.skype.com/%s/%s" style="border: none;" alt="My status" />
</a>
"""

SKYPE_WIDGET_TYPES = {
    'small': 'smallclassic',
    'big': 'bigclassic',
    'balloon': 'balloon',
    'smallicon': 'smallicon',
    'bigicon': 'mediumicon',
}


@register.simple_tag
def skype(id, flags=''):
    """
    renders skype widget
    http://www.skype.com/intl/en/share/buttons/
    http://www.skype.com/intl/en/share/buttons/advanced.html
    """
    if not id:
        #don't render, no id passed
        return ''

    flags = set(f.strip() for f in flags.split(','))

    type = SKYPE_WIDGET_TYPES.values()[0]

    for typename in SKYPE_WIDGET_TYPES:
        if typename in flags:
            type = SKYPE_WIDGET_TYPES[typename]

    return mark_safe(SKYPE_WIDGET_TEMPLATE % (id, type, urllib.quote(id)))

