from django.contrib import admin
from treemenus.admin import MenuAdmin
from treemenus.admin import MenuItemAdmin
from treemenus.models import Menu
from .models import MenuItemExt

class MenuItemExtInline(admin.StackedInline):
    model = MenuItemExt
    extra = 0

class CustomMenuItemAdmin(MenuItemAdmin):
    inlines = [MenuItemExtInline,]


class CustomMenuAdmin(MenuAdmin):
    menu_item_admin_class = CustomMenuItemAdmin


# Unregister the standard admin options
admin.site.unregister(Menu)

# Register the new admin options
admin.site.register(Menu, CustomMenuAdmin)