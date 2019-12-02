from django.test import TestCase
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django_redis import get_redis_connection

import datetime
from django.utils import timezone
# Create your tests here.
from server.models import *

# Django的单元测试基于unittest库


class AuthTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        WebUser.objects.create_user('test1234', password='test1234')

    def test_first_wx_login(self):
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
        print(response.json())
        assert response.status_code == 200

    def test_web_login(self):
        client = APIClient()
        response = client.post(
            '/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()


class ProjectTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        WebUser.objects.create_user('test1234', password='test1234')

    def test_create_project(self):
        client = APIClient()
        response = client.post(
            '/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200
        # filename = 'cover.jpg'
        # file = File(open('media/cover.jpg', 'rb'))
        # uploaded_file = SimpleUploadedFile(filename, file.read(), content_type='multipart/form-data')
        response = client.post('/project/detail', {
            "title": "标题",
            "content": "详情",
            # "cover": uploaded_file,
            "require_num": 100,
            "requirements": "需求",
            "form": "{json文本}",
            "deadline": '2019-12-12 09:00:00'
        })
        # print(response)
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()

class CheckTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        WebUser.objects.create_user('test1234', password='test1234')

        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111,name='清小华', department='软件学院', email='lixiaojia@163.com', phone=12233)
        _user.save()
        _project = Project(id=1,title='test', content='testcontent', require_num=12, requirements='req', deadline=datetime.datetime(2019,12,1,23,59,59))
        _project.save()

        ApplyRecord.objects.create(id=1,user=_user,project=_project,form='{json文本}',status='W')

    def test_viewapplyinfo(self):
        client = APIClient()
        response = client.post(
            '/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

        response = client.get('/check/ViewApplyInfo', {'project_id':1})
        assert response.status_code == 200

    def test_checkop(self):
        client = APIClient()
        response = client.post(
            '/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

        response = client.post('/check/CheckOp', {'apply_id':1, 'checked':True})
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()

class ApplyTestCase(TestCase):
    def setUp(self):
        WxUser.objects.create(id=2017011111,name='清小华', department='软件学院', email='lixiaojia@163.com', phone=12233)
        Project.objects.create(title='test', content='testcontent', require_num=12, requirements='req', deadline=datetime.datetime(2019,12,1,23,59,59))
    
    def test_fillform(self):
        client = APIClient()
        response = client.post('/auth/login', {'token':'null'})
        assert response.status_code == 200

        response = client.post('/apply/fillform', {'project_id':1, 'form':'{json文本}'})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()

class CancelApplyTestCase(TestCase):
    def setUp(self):
        _user = WxUser(id=2017011111,name='清小华', department='软件学院', email='lixiaojia@163.com', phone=12233)
        _user.save()
        _project = Project(title='test', content='testcontent', require_num=12, requirements='req', deadline=datetime.datetime(2019,12,1,23,59,59))
        _project.save()

        ApplyRecord.objects.create(id=1,user=_user,project=_project,form='{json文本}',status='W')
    def test_cancelapply(self):
        client = APIClient()

        response = client.post('/auth/login', {'token':'null'})
        assert response.status_code == 200

        response = client.post('/apply/cancelapply',{'apply_id':1})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()

class signinTestCase(TestCase):
    def setUp(self):
        _user = WxUser.objects.create(id=2017011111,name='清小华', department='软件学院', email='lixiaojia@163.com', phone=10086)
        _project = Project.objects.create(title='test', content='testcontent', require_num=12, requirements='req', deadline=datetime.datetime(2019,12,1,23,59,59))
        _join_record = JoinRecord.objects.create(user=_user,project=_project)
        _sign_project=SignProject.objects.create(project=_project, title='第一次活动', content='content', begin_time=timezone.now() + datetime.timedelta(minutes=1), end_time=timezone.now())

    def test_signin(self):
        client = APIClient()
        response = client.post('/auth/login', {'token':'null'})
        assert response.status_code == 200

        response = client.post('/sign/signin', {'sign_project':1})
        assert response.status_code == 200

        response = client.post('/sign/signin', {'sign_project':1})
        assert response.status_code == 409

    def tearDown(self):
        get_redis_connection("default").flushall()

class signoutTestCase(TestCase):
    def setUp(self):
        _user = WxUser(id=2017011111,name='清小华', department='软件学院', email='lixiaojia@163.com', phone=12233)
        _user.save()

        _project = Project(title='test', content='testcontent', require_num=12, requirements='req', deadline=datetime.datetime(2019,12,1,23,59,59))
        _project.save()
        
        _join_record = JoinRecord(user=_user,project=_project)
        _join_record.save()

        _sign_project=SignProject(project=_project, title='第一次活动', content='content', begin_time=timezone.now(), end_time=timezone.now())
        _sign_project.save()

        SignRecord.objects.create(id=1, join_record=_join_record, sign_project=_sign_project)

    def test_signout(self):
        client = APIClient()
        response = client.post('/auth/login', {'token':'null'})
        assert response.status_code == 200

        response = client.post('/sign/signout', {'sign_record_id':1})
        assert response.status_code == 200
    def tearDown(self):
        get_redis_connection("default").flushall()
