from django.shortcuts import render_to_response
from django.template.context import RequestContext

from .models import Lecture

#def agenda(request):
#    data = {
#        'lectures': Lecture.objects.filter(is_disabled=False),
#        ''
#    }
#    return render_to_response('conference/agenda.html', data, context_instance=RequestContext(request))