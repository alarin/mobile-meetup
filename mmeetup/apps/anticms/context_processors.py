from operator import attrgetter
from django.utils.translation import get_language

from treemenus.models import Menu
from .models import MenuItemExt

def menu(request):
    submenu = None
    try:
        # Select all top-level menu items for current language
        lang = get_language()
        menu_items = MenuItemExt.objects.filter(
            language=lang, menu_item__level = 1).select_related()
    except Menu.DoesNotExist:
        # Return nothing
        return {'menu': {}, 'submenu': {}}

    # Find selected menu item and children
    selected = None
    sorted_menu_items = sorted(menu_items,
                               key=lambda item: len(item.menu_item.url),
                               reverse=True)
    for item in sorted_menu_items:
        # Select menu item by url
        if request.path.startswith(item.menu_item.url):
            item.selected = True
            selected = item
            submenu = MenuItemExt.objects.filter(
                language=lang,
                menu_item__parent=selected.menu_item).select_related()
            break
    
    # Find selected submenu
    if submenu:
        for subitem in submenu:
            if subitem.menu_item.url == request.path:
                subitem.selected = True
                selected = item.menu_item

    return {'menu': menu_items,
            'submenu': submenu,
            'menu_item': selected }
