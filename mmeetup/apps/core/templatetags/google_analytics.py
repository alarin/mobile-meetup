from django import template
from django.conf import settings

register = template.Library()

def simple_minify(src):
    lines = []
    for line in src.splitlines():
        line = line.strip();
        if not line.startswith('//'):
            lines.append(line)

    return ''.join(lines)

def google_analytics_js():
    code =  getattr(settings, "GOOGLE_ANALYTICS_CODE", False)
    minify = getattr(settings, "GOOGLE_ANALYTICS_MINIFY", True)

    if not code:
        return "<!-- Goggle Analytics not included because you haven't set the settings.GOOGLE_ANALYTICS_CODE variable! -->"

    if settings.DEBUG:
        return "<!-- Goggle Analytics not included because you are in Debug mode! -->"

    # todo: don't show if currently logged in user is staff, but don't know how to check request.user.is_staff at this point?
    # if someone tells me where to get the request object from, I'll edit this!


    pagetrack_code = """
        //track russian and ukrainian search engines
        engines = [
            ["rambler.ru","words"],
            ["nova.rambler.ru","query"],
            ["mail.ru","q"],
            ["go.mail.ru","q"],
            ["search.otvet.mail.ru","q"],
            ["aport.ru","r"],
            ["metabot.ru","st"],
            ["meta.ua","q"],
            ["bigmir.net","q"],
            ["nigma.ru","s"],
            ["search.ukr.net","search_query"],
            ["start.qip.ru","query"],
            ["gogle.com.ua","q"],
            ["google.com.ua","q"],
            ["images.google.com.ua","q"],
            ["search.winamp.com","query"],
            ["search.icq.com","q"],
            ["m.yandex.ru","query"],
            ["gde.ru","keywords"],
            ["genon.ru","QuestionText"],
            ["blogs.yandex.ru", "text"],
            ["webalta.ru", "q"],
            ["akavita.by", "z"],
            ["meta.ua", "q"],
            ["tut.by", "query"],
            ["all.by", "query"],
            ["i.ua", "q"],
            ["online.ua", "q"],
            ["a.ua", "s"],
            ["ukr.net", "search_query"],
            ["search.com.ua", "q"],
            ["search.ua", "query"],
            ["poisk.ru", "text"],
            ["km.ru", "sq"],
            ["liveinternet.ru", "ask"],
            ["gogo.ru", "q"],
            ["quintura.ru", "request"]
        ];
        for (var i=0; i < engines.length; i++) {
            _gaq.push(['_addOrganic', engines[i][0], engines[i][1]]);
        };
    """
    gacode = """
    <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', '%(uacct)s']);
      _gaq.push(['_trackPageview']);
      _gaq.push(['_trackPageLoadTime']);
      %(pagetrack)s
      
      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>
    """ % { 'uacct': code, 'pagetrack': pagetrack_code}

    if minify:
        gacode = simple_minify(gacode)
    return gacode
register.simple_tag(google_analytics_js)