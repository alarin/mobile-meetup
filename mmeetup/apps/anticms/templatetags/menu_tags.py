from django import template

register = template.Library()

@register.inclusion_tag('treemenus/_menu.html')
def display_menu(menu):
    return {'menu': menu}