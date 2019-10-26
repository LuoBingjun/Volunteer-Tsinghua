from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from server.models import User

def login_required(func):
    def wrapper(self, *args, **kargs):
        request = self.request
        id = request.session.get('user')
        user = User.objects.filter(pk=id)
        if user.exists():
            request.user = User.objects.get(pk=id)
            return func(self, *args, **kargs)
        else:
            raise PermissionDenied()
    return wrapper
