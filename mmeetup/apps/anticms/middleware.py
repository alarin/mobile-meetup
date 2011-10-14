from django.http import HttpResponse
from django.template.context import RequestContext
from django.template import loader
from django.template import TemplateDoesNotExist
from .models import MenuItemExt
from django.utils.translation import get_language

class MenuMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response

        try:
            # Get menu item template name from request.path
            lang = get_language()
            item = MenuItemExt.objects.filter(menu_item__url=request.path, language=lang).get()
        except MenuItemExt.DoesNotExist:
            return response

        if not item.template:
            return response

        try:
            # Load template
            t = loader.get_template(item.template.name)
        except TemplateDoesNotExist:
            return response
        
        c = RequestContext(request, {})
        return HttpResponse(t.render(c))