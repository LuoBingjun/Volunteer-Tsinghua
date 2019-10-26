from rest_framework.response import Response

from server.models import User

def login_required(func):
    def wrapper(self, request):
        try:
            id = request.session['user']
            request.user = User.objects.get(pk=id)
            return func(self, request)
        except:
            return Response(status=403)
    return wrapper
