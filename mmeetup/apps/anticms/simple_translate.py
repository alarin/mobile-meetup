from simple_translation.translation_pool import translation_pool

from treemenus.models import MenuItem
from models import MenuItemExt

translation_pool.register_translation(MenuItem, MenuItemExt)
