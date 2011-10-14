def is_https(request):
    return request.META.get('HTTPS') or request.META.get('wsgi.url_scheme') == 'https'