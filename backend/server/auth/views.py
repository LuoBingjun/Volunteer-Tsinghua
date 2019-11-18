from django.contrib import auth
from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import RetrieveAPIView

from django.shortcuts import get_object_or_404

import json
import requests

from backend import settings
from server.models import *
from server.utils import login_required

class preloginSerializer(serializers.Serializer):
    code = serializers.CharField()

class preloginView(APIView):
    def post(self, request):
        serializer = preloginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        errcode = -1
        while errcode == -1:
            response = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(settings.APPID, settings.APPSECRET, code)).json()
            errcode = response.get('errcode')
        
        openid = response.get('openid')
        if not openid:
            return Response(status=400)
        
        #request.session.cycle_key()
        request.session['openid'] = openid

        print(openid)

        user = WxUser.objects.filter(openid=openid)
        if user.exists():
            request.session['wx_user'] = user[0].id
            login_status = True
        else:
            login_status = False

        return Response({
            'login_status':login_status
        })



class loginSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128)


class loginView(APIView):
    def post(self, request):
        info = loginSerializer(data=request.data)
        if info.is_valid():
            token = info.validated_data['token']
            userinfo = self.get_userinfo(token)

            #request.session.cycle_key()
            openid = request.session.get('openid')
            request.session['wx_user'] = int(userinfo['card'])

            user = WxUser.objects.filter(pk=userinfo['card'])
            if user.exists():
                first_login = False
                users = WxUser.objects.filter(openid=openid)
                users.update(openid=None)

                user = WxUser.objects.get(pk=userinfo['card'])
                user.openid = openid
                user.save()
            else:
                first_login = True

            response = Response({
                'first_login': first_login,
                'name': userinfo['name'],
                'id': userinfo['card'],
                'department': userinfo['department']
            })
            
            #response['Set-Cookie'] = 'sessionid={0}; Path=/'.format(request.session.session_key)
            return response
        else:
            return Response(info.errors, status=400)

    def get_userinfo(self, token):
        if token == 'null':
            return {
                'name': '清小华',
                'card': 2017011111,
                'department': '软件学院'
            }
        # print(token)
        params = {
            'token': token
        }
        # headers = {'content_type':'application/json'}
        response = requests.post(
            'https://alumni-test.iterator-traits.com/fake-id-tsinghua-proxy/api/user/session/token', json=params).json()
        print(response)
        userinfo = response.get('user')
        return userinfo

class webloginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)

class webloginView(APIView):
    def post(self, request):
        info = webloginSerializer(data=request.data)
        info.is_valid(raise_exception=True)
        username = info.validated_data['username']
        password = info.validated_data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.logout(request)
            auth.login(request, user)
            response = Response(status=200)
            # response['Set-Cookie'] = 'sessionid={0}; Path=/'.format(
            #     request.session.session_key)
            return response
        else:
            return Response('Login failed.', status=406)


class postUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        fields = ['id', 'name', 'department', 'email', 'phone']


class getUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        exclude = ['join_time']


class putUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WxUser
        fields = ['department', 'email', 'phone']


class userView(APIView):
    def post(self, request):
        id = request.session.get('wx_user')
        if not id:
            raise PermissionDenied()
        serializer = postUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.openid = request.session.get('openid')
        user.save()
        return Response(serializer.data)

    @login_required(wx=True)
    def put(self, request):
        serializer = putUserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @login_required(wx=True)
    def get(self, request):
        serializer = getUserSerializer(request.user)
        return Response(serializer.data)
