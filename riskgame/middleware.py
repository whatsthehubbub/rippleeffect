from django.http import HttpResponsePermanentRedirect

class WWWRedirectMiddleware(object):
    def process_request(self, request):
        # Check that we're not on the dev server
        # And check if there isn't www in front of the URL
        if not request.META['HTTP_HOST'].startswith('127.') and not request.META['HTTP_HOST'].startswith('www.') and not request.META['HTTP_HOST'].startswith('192'):
            return HttpResponsePermanentRedirect('http://www.playrippleeffect.com')

# from riskgame.models import Game
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
# from django.conf import settings

# class PreLaunchMiddleware(object):
#     def process_request(self, request):
#         game = Game.objects.get_latest_game()

#         if request.path.startswith(settings.STATIC_URL) or request.path.startswith('/admin') or request.path.startswith('/accounts/login') or request.path.startswith(reverse('pre_launch')):
#             return None

#         if not game.started: # Pre launch situation
#             if request.user.is_authenticated():
#                 return None
#             else:
#                 return HttpResponseRedirect(reverse('pre_launch'))

from django.contrib.auth import get_user_model

class ImpersonateMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and request.user.is_admin and "impersonate" in request.GET:
            request.session['impersonate_email'] = request.GET["impersonate"]
        elif "unimpersonate" in request.GET and 'impersonate_email' in request.session:
            del request.session['impersonate_email']

        if request.user.is_authenticated() and request.user.is_admin and 'impersonate_email' in request.session:

            UserModel = get_user_model()
            try:
                request.user = UserModel.objects.get(email=request.session['impersonate_email'])
            except UserModel.DoesNotExist:
                del request.session['impersonate_email']
