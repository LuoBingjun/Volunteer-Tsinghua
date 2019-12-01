from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

import requests
import time

from server.models import WxUser, WebUser
from backend import settings

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


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


def get_AccessToken():
    access_token = cache.get('access_token')
    print(access_token)
    if not (access_token and access_token['expire_time'] >= int(time.time())):
        errcode = -1
        while errcode == -1:
            response = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(
                settings.APPID, settings.APPSECRET)).json()
            errcode = response.get('errcode')

        if response.get('access_token') and response.get('expires_in'):
            access_token = {
                'access_token': response['access_token'],
                'expire_time': int(time.time()) + response['expires_in']
            }
            cache.set('access_token', access_token)
        else:
            raise ImproperlyConfigured()
    return access_token['access_token']


def send_wx_msg(touser, template_id, page, data):
    access_token = get_AccessToken()
    response = requests.post('https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={0}'.format(access_token), json={
        'touser': touser.openid,
        'template_id': template_id,
        'page': page,
        'data': data
    }).json()

    errcode = response.get('errcode')
    if errcode:
        return response
    else:
        return 0

def test():
    send_wx_msg(WxUser.objects.get(id=2017011111), 'JRmcDj_rRLknyYVevU-iNgosYQ7cm88cs2UTS89B2-o',
            '',
            {
                'phrase1': {"value": '审核通过'},
                "thing2": {"value": '活动名称'},
                "time3": {"value": '2019-10-01 15:01'},
                "thing5": {'value': '温馨提示'},
                "name4": {'value': '申请人'}}
            )

    send_wx_msg(WxUser.objects.get(id=2017011111), 'z7xt4wI2pFXsbFsI3pdDhzJ5LYcQh9KU5EaiOKg1aRM',
            '',
            {
                'thing1': {"value": '审核通过'},
                "date2": {"value": '2019-10-01'},
                "thing4": {"value": '签到地点'},
                "time3": {'value': '2019-10-01 15:01'},
            })
