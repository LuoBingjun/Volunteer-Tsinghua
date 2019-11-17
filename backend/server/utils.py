from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from server.models import WxUser, WebUser

# from django.contrib.auth import decorators

def login_required(web=False, wx=False):
    def wrapper(func):
        def web_func(self, *args, **kargs):
            request = self.request
            if request.user.is_authenticated:
                return func(self, *args, **kargs)
            else:
                raise PermissionDenied()

        def wx_func(self, *args, **kargs):
            request = self.request
            id = request.session.get('wx_user')
            user = WxUser.objects.filter(pk=id)
            if user.exists():
                request.user = user[0]
                return func(self, *args, **kargs)
            else:
                raise PermissionDenied()

        def inner(self, *args, **kargs):
            request = self.request
            if web and wx:
                if request.session.get('wx_user'):
                    return wx_func(self, *args, **kargs)
                else:
                    return web_func(self, *args, **kargs)
            elif web:
                return web_func(self, *args, **kargs)
            elif wx:
                return wx_func(self, *args, **kargs)
        return inner
    return wrapper

from rest_framework.authentication import SessionAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return