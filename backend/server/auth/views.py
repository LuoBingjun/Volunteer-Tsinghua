from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth


from server.models import *
from server.utils import login_required
# import requests


class loginSerializer(serializers.Serializer):
    ticket = serializers.CharField(max_length=128)

class loginView(APIView):
    def post(self, request):
        info = loginSerializer(data=request.data)
        if info.is_valid():
            ticket = info.validated_data['ticket']
            if request._request.META.__contains__('HTTP_X_FORWARDED_FOR'):
                ip =  request._request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request._request.META['REMOTE_ADDR']
            userinfo = self.get_userinfo(ticket, ip)
            user = User.objects.filter(pk=userinfo['id'])
            if user.exists():
                user = user[0]
                first_login = False
            else:
                user = User(**userinfo)
                user.save()
                first_login = True
            request.session.cycle_key()
            request.session['user'] = int(user.id)
            response = Response({
                'first_login': first_login,
                'name': userinfo['name'],
                'id': userinfo['id'],
                'department': userinfo['department']
            })
            response['Set-Cookie'] = 'sessionid=' + \
                request.session.session_key+';Path=/'
            return response
        else:
            return Response(info.errors, status=400)

    def get_userinfo(self, ticket, ip):
        # response = requests.get('https://id.tsinghua.edu.cn/thuser/authapi/checkticket/{0}/{1}/{2}'.format(1234, ticket, ip))
        return {
            'id': 2017013573,
            'name': '清小华',
            'department': '软件学院',
            'email': 'lbj17@mails.tsinghua.edu.cm'
        }
