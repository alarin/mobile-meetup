from dbtemplates.models import Template
from django.db import models
from treemenus.models import MenuItem
from django.conf import settings


# Localized menu item
class MenuItemExt(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name='ext')
    # Menu item language
    language = models.CharField(max_length=255, choices=settings.LANGUAGES)
    # Localized menu item caption
    caption = models.CharField(max_length=50)
    # Link to menu item template
    template = models.ForeignKey(Template, blank=True, null=True)
    
    class Meta:
        ordering = ('menu_item__rank',)
        unique_together = (('menu_item', 'language'),)