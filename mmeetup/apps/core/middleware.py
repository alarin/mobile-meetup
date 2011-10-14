from django.http import HttpResponseRedirect
from django.conf import settings

from core.utils import is_https


class HttpsOnlyAuthMiddleware():
    def process_request(self, request):
        if not is_https(request) and request.user.is_authenticated():
            return HttpResponseRedirect('https://%s%s' % (request.get_host(), request.path))
        
        return None
