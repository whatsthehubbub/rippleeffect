from django.http import HttpResponse
from django.template import RequestContext, loader
# from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    t = loader.get_template('index.html')
    
    c = RequestContext(request, {})

    return HttpResponse(t.render(c))
