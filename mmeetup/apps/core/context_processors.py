def browser(request):
    """
    Determine user browser depends on HTTP_USER_AGENT.
    Thanks jquery for idea
    """
    browser = {}
    
    if not 'HTTP_USER_AGENT' in request.META:
        return {}
    
    ua = request.META['HTTP_USER_AGENT'].lower()
    
    browser['safari'] = ua.find('webkit') != -1
    browser['opera'] = ua.find('opera') != -1
    browser['msie'] = (ua.find('msie') != -1) and (ua.find('opera') == -1)
    browser['mozilla'] = (ua.find('mozilla') != -1) and (ua.find('compatible') == -1) and (ua.find('webkit') == -1)

    return {'browser': browser}


def sitename(request):
    from django.contrib.sites.models import Site
    return {'sitename': Site.objects.get_current().domain}
