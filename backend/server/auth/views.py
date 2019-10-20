from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from server.models import *


class loginSerializer(serializers.Serializer):
    ticket = serializers.CharField(max_length=128)


class loginView(APIView):
    def post(self, request):
        info = loginSerializer(data=request.data)
        if info.is_valid():
            ticket = info.validated_data['ticket']
            userinfo = self.get_userinfo(ticket)
            user = User.objects.filter(pk=userinfo.id, is_staff=False)
            if user.exists():
                user = user[0]
                first_login = False
            else:
                user = User(**usrinfo)
                user.save()
                first_login = True
            request.session['user'] = user
            response = Response({
                'first_login': first_login,
                'name': userinfo['user'],
                'id': userinfo['id'],
                'department': userinfo['deparment']
            })
            response['Set-Cookie'] = 'sessionid=' + \
                request.session.session_key+';Path=/'
            return response
        else:
            return Response(info.errors, status=400)

    def get_userinfo(self, ticket):
        return {
            'id': 2017013573,
            'name': '清小华',
            'department': '软件学院',
            'email': 'lbj17@mails.tsinghua.edu.cm'
        }
