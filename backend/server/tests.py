from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory

# Create your tests here.
from server.models import *

# Django的单元测试基于unittest库
class AuthTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        pass

    def test_first_login_and_register(self):
        client = APIClient()
        response = client.post('/auth/login', {'token': 'null'})
        assert response.status_code == 200
        assert response.data.get('first_login') == True
        response = client.post('/auth/user', {
            'name': '清小华',
            'id': 2017011111,
            'department': '软件学院',
            'email': 'xxh17@mails.tsinghua.edu.cn',
            'phone': '13888888888'
        })
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        pass
