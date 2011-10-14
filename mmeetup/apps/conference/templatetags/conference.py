from django import template
from django.template.defaultfilters import register

from .. models import Lecture, Partner


class GetAgendaNode(template.Node):
    def render(self, context):
        context['lectures'] = Lecture.objects.filter(is_disabled=False).select_related()
        return ''


@register.tag
def get_agenda(parser, token):
    return GetAgendaNode()


class GetPartnersNode(template.Node):
    def render(self, context):
        context['partners'] = Partner.objects.select_related()
        return ''


@register.tag
def get_partners(parser, token):
    return GetPartnersNode()