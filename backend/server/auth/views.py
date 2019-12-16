from Crypto.Cipher import AES
import base64
from Crypto import Random
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import RetrieveAPIView, ListAPIView

from django.shortcuts import get_object_or_404

import json
import requests

from backend import settings
from server.models import *
from server.utils import login_required

from server.auth.identicon import *

import random
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
class preloginSerializer(serializers.Serializer):
    code = serializers.CharField()


class preloginView(APIView):
    def post(self, request):
        serializer = preloginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']

        errcode = -1
        while errcode == -1:
            response = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(
                settings.APPID, settings.APPSECRET, code)).json()
            errcode = response.get('errcode')

        openid = response.get('openid')
        if not openid:
            return Response(status=400)

        request.session.cycle_key()
        request.session['openid'] = openid

        print(openid)

        user = WxUser.objects.filter(openid=openid)
        if user.exists():
            request.session['wx_user'] = user[0].id
            login_status = True
        else:
            login_status = False

        return Response({
            'login_status': login_status
        })


class loginSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128)


class loginView(APIView):
    def post(self, request):
        info = loginSerializer(data=request.data)
        if info.is_valid():
            token = info.validated_data['token']
            userinfo = self.get_userinfo(token)

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
            response = Response({
                'is_superuser': user.is_superuser
            }, status=200)
            return response
        else:
            return Response('Login failed.', status=406)


class postUserSerializer(serializers.ModelSerializer):
    id_card = serializers.RegexField(r'\d{17}[0-9Xx]')

    class Meta:
        model = WxUser
        fields = ['id', 'name', 'department', 'email', 'phone', 'id_card']


class getUserSerializer(serializers.ModelSerializer):
    id_card = serializers.SerializerMethodField()

    class Meta:
        model = WxUser
        exclude = ['join_time']

    def get_id_card(self, obj):
        key = settings.SECRET_KEY.encode('utf-8')[:32]
        cipher = AES.new(key, AES.MODE_ECB)
        return decode(cipher, obj.id_card)


class putUserSerializer(serializers.ModelSerializer):
    id_card = serializers.RegexField(r'\d{17}[0-9Xx]')
    class Meta:
        model = WxUser
        fields = ['department', 'email', 'phone', 'id_card']


BLOCK_SIZE = 32
PADDING = '{'
def pad(s): 
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
def encode(c, s):
    return base64.b64encode(c.encrypt(pad(s).encode('utf-8'))).decode('utf-8')
def decode(c, e): 
    return c.decrypt(base64.b64decode(e.encode('utf-8'))).decode('utf-8').rstrip(PADDING)


class userView(APIView):
    def post(self, request):
        id = request.session.get('wx_user')
        if not id:
            raise PermissionDenied()
        serializer = postUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = settings.SECRET_KEY.encode('utf-8')[:32]
        cipher = AES.new(key, AES.MODE_ECB)
        # encoded = encode(cipher, serializer.validated_data['id_card'])
        # s = decode(cipher, encoded)
        # assert serializer.validated_data['id_card'] == s
        serializer.validated_data['id_card'] = encode(cipher, serializer.validated_data['id_card']) 
        user = serializer.save()
        user.openid = request.session.get('openid')
        user.save()
        return Response(serializer.data)

    @login_required(wx=True)
    def put(self, request):
        serializer = putUserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        key = settings.SECRET_KEY.encode('utf-8')[:32]
        cipher = AES.new(key, AES.MODE_ECB)
        serializer.validated_data['id_card'] = encode(cipher, serializer.validated_data['id_card'])
        serializer.save()
        return Response(serializer.data)

    @login_required(wx=True)
    def get(self, request):
        serializer = getUserSerializer(request.user)
        return Response(serializer.data)


class postWebuserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    class Meta:
        model = WebUser
        fields = ['username', 'password', 'name',
                  'description', 'manager', 'email', 'phone', 'avatar']


class putWebuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ['name', 'description', 'manager', 'email', 'phone', 'avatar']


class getWebuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ['id', 'name', 'description', 'manager', 'email', 'phone', 'avatar']


class webuserView(APIView):
    @login_required(web=True)
    def post(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied()
        serializer = postWebuserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not request.data.get('avatar'):
            avatar = render_identicon(random.randint(1,100000)*10000000+random.randint(1,10000000), 16)  
            f=BytesIO()
            avatar.save(f,'JPEG')
            file = InMemoryUploadedFile(f, None, 'avatar.jpg', None, 48, None, None)       
            serializer.validated_data['avatar']=file
        else:
            serializer.validated_data['avatar']=request.FILES.get('avatar')


        WebUser.objects.create_user(**serializer.validated_data)
        return Response(status=200)

    @login_required(web=True)
    def delete(self, request):
        if not request.user.is_superuser:
            raise PermissionDenied()
        id = request.query_params.get('id')
        user = get_object_or_404(WebUser, pk=id)
        user.delete()
        return Response(status=200)

    @login_required(web=True)
    def put(self, request):
        id = request.query_params.get('id')
        if id:
            if not request.user.is_superuser:
                raise PermissionDenied()
            user = get_object_or_404(WebUser, pk=id)
        else:
            user = request.user
        serializer = putWebuserSerializer(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @login_required(web=True)
    def get(self, request):
        id = request.query_params.get('id')
        if id:
            user = get_object_or_404(WebUser, pk=id)
        else:
            user = request.user
        serializer = getWebuserSerializer(user)
        return Response(serializer.data)


class listWebuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebUser
        fields = ['id', 'name', 'description', 'manager', 'email', 'phone']


class listwebuserView(ListAPIView):
    serializer_class = listWebuserSerializer
    @login_required(web=True)
    def get_queryset(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied()
        return WebUser.objects.all()


class unbundlingView(APIView):
    @login_required(wx=True)
    def post(self, request):
        request.user.openid = None
        request.user.save()
        return Response(status=200)

# class testView(APIView):

#     def post(self,request):
#         img = render_identicon(2017013627, 16)
#         img.save('123123.png')
#         # im = Image.open('123123.png')
#         # im_rotate_180 = im.transpose(Image.FLIP_LEFT_RIGHT)
#         # im.paste(im_rotate_180,(48,48),None)
#         return Response(status=200)