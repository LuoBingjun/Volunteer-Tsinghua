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

# 14
# 普通用户登录
# 管理员登录
# 发起项目
# 查看项目详情
# 查看项目列表
# 搜索项目
# 取消项目
# 查看报名信息
# 审核操作
# 报名
# 取消报名
# 发起签到
# 签到
# 签退


class AuthTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        WebUser.objects.create_user('test1234', password='test1234')

    # 普通用户登录
    def test_first_wx_login(self):
        client = APIClient()
        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200
        assert response.data.get('first_login') == True
        response = client.post('/api/auth/user', {
            'name': '清小华',
            'id': 2017011111,
            'department': '软件学院',
            'email': 'xxh17@mails.tsinghua.edu.cn',
            'phone': '13888888888',
            'id_card':'11111119990000000x'
        })
        assert response.status_code == 200
        response = client.get('/api/auth/user')
        assert response.status_code == 200

    # 管理员登录
    def test_web_login(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()


class ProjectCreateTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        WebUser.objects.create_user('test1234', password='test1234')
    # 发起项目

    def test_create_project(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200
        # file = File(open('media/cover.jpg', 'rb'))
        # uploaded_file = SimpleUploadedFile(
        #     'cover.jpg', file.read(), content_type='multipart/form-data')
        response = client.post('/api/project/detail', {
            "title": "题目",
            "content": "内容",
            "introduction": "简介",
            "requirements": "需求",
            "type":'QT',
            "form": "{}",
            "loc":"loc",
            "cover": open('media/cover.jpg', 'rb'),
            "qrcode_1":open('media/cover.jpg', 'rb'),
            "qrcode_2":open('media/cover.jpg', 'rb'),
            "success_note":'温馨提示',
            "deadline": "2035-12-3 12:00:00",
            "begin_datetime": "2019-12-4 13:00:00",
            "end_datetime": "2035-12-5 18:00:00",
            "jobs": '''[{
				    "job_name":"job1", 
				    "job_worktime":2.5, 
				    "job_content":"job1content1", 
				    "job_require_num":250 
			    }, 
			    { 
				    "job_name":"job2", 
				    "job_worktime":250.0, 
				    "job_content":"job2content2",
				    "job_require_num":25
			    }]'''
        })
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()


class ProjectTestCase(TestCase):
    def setUp(self):
        admin1 = WebUser.objects.create_user(
            id=1, username='admin1', password='admin1')
        _user = WxUser.objects.create(
            id=2017011111, name='清小华', department='软件学院', email='lixiaojia@163.com', phone=12233, id_card='11111119990000000X')
        # 在ApplyRecord中创建一条记录
        _project = Project.objects.create(id=1, webuser=admin1, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                                          begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        _job = Job.objects.create(id=1, project=_project, job_name='test_job',
                                  job_worktime=5.0, job_content='content_test', job_require_num=10)

    # 查看项目详情
    def test_projectdetail(self):
        client = APIClient()

        response = client.post(
            '/api/auth/weblogin', {'username': 'admin1', 'password': 'admin1'})
        assert response.status_code == 200

        response = client.get('/api/project/detail', {'id': 1})
        assert response.status_code == 200
        assert response.data.get('content') == 'testcontent'

        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.get('/api/project/detail', {'id': 1})
        assert response.status_code == 200
        # assert response.data.get('title') == 'test'

    # 查看项目列表
    def test_projectlist(self):
        client = APIClient()

        response = client.post(
            '/api/auth/weblogin', {'username': 'admin1', 'password': 'admin1'})
        assert response.status_code == 200

        response = client.get('/api/project/list')
        assert response.status_code == 200

        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.get('/api/project/list')
        assert response.status_code == 200

    # 搜索项目
    def test_searchproject(self):
        client = APIClient()

        response = client.post(
            '/api/auth/weblogin', {'username': 'admin1', 'password': 'admin1'})
        assert response.status_code == 200

        response = client.get('/api/project/list', {"search": "tset"})
        assert response.status_code == 200

        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.get('/api/project/list', {"search": "tset"})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()


class ProjectCancelTestCase(TestCase):
    def setUp(self):
        admin1 = WebUser.objects.create_user(
            id=1, username='admin1', password='admin1', is_superuser=True)
        admin2 = WebUser.objects.create_user(
            id=2, username='admin2', password='admin2', is_superuser=False)

        # 在ApplyRecord中创建一条记录

        _project_admin1_1 = Project.objects.create(id=1, webuser=admin1, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                                                   begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))

        _job = Job.objects.create(id=1, project=_project_admin1_1, job_name='test_job',
                                  job_worktime=5.0, job_content='content_test', job_require_num=10)

        Project.objects.create(id=2, webuser=admin1, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                               begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        Project.objects.create(id=3, webuser=admin2, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                               begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        Project.objects.create(id=4, webuser=admin2, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                               begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))

    # 取消项目

    def test_cancelproject(self):
        client = APIClient()

        response = client.post(
            '/api/auth/weblogin', {'username': 'admin2', 'password': 'admin2'})
        assert response.status_code == 200

        response = client.post('/api/project/cancel', {'project_id': 1})
        assert response.status_code == 404

        response = client.post('/api/project/cancel', {'project_id': 2})
        assert response.status_code == 404

        response = client.post('/api/project/cancel', {'project_id': 3})
        assert response.status_code == 200

        response = client.post(
            '/api/auth/weblogin', {'username': 'admin1', 'password': 'admin1'})
        assert response.status_code == 200

        response = client.post('/api/project/cancel', {'project_id': 1})
        assert response.status_code == 200

        response = client.post('/api/project/cancel', {'project_id': 2})
        assert response.status_code == 200

        response = client.post('/api/project/cancel', {'project_id': 3})
        assert response.status_code == 404

        response = client.post('/api/project/cancel', {'project_id': 4})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()


class CheckTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111, name='清小华', department='软件学院',
                       email='lixiaojia@163.com', phone=12233, id_card='11111119990000000X')
        _user.save()
        _project = Project(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                           begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        _project.save()
        _job = Job(id=1, project=_project, job_name='test_job',
                   job_worktime=5.0, job_content='content_test', job_require_num=10)
        _job.save()

        ApplyRecord.objects.create(
            id=1, user=_user, job=_job, project=_project, form='{json文本}', status='W')

    # 查看报名信息
    def test_viewapplyinfo(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

        response = client.get('/api/check/ViewApplyInfo', {'project_id': 1})
        assert response.status_code == 200

    # 审核操作

    def test_checkop(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

        response = client.post(
            '/api/check/CheckOp', {'apply_id': 1, 'checked': True})
        assert response.status_code == 200

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()


class ApplyTestCase(TestCase):
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111, name='清小华', department='软件学院',
                       email='lixiaojia@163.com', phone=12233, id_card='11111119990000000X')
        _user.save()
        _project = Project(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                           begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        _project.save()
        _job = Job(id=1, project=_project, job_name='test_job',
                   job_worktime=5.0, job_content='content_test', job_require_num=10)
        _job.save()

    # 报名
    def test_fillform(self):
        client = APIClient()
        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.post(
            '/api/apply/fillform', {'job_id': 1, 'form': '{json文本}'})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()


class CancelApplyTestCase(TestCase):
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111, name='清小华', department='软件学院',
                       email='lixiaojia@163.com', phone=12233)
        _user.save()
        _project = Project(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req', deadline=datetime.datetime(2035, 12, 1, 23, 59, 59),
                           begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0), end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        _project.save()
        _job = Job(id=1, project=_project, job_name='test_job',
                   job_worktime=5.0, job_content='content_test', job_require_num=10)
        _job.save()

        ApplyRecord.objects.create(
            id=1, user=_user, job=_job, project=_project, form='{json文本}', status='W')

    # 取消报名
    def test_cancelapply(self):
        client = APIClient()

        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.post('/api/apply/cancelapply', {'project_id': 1, 'job_id':1})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()


class signprojectTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _project = Project.objects.create(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req',
                                          deadline=datetime.datetime(2035, 12, 1, 23, 59, 59), begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0),
                                          end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59))
        Job.objects.create(id=2, project=_project, job_name='test_job',
                           job_worktime=5.0, job_content='content_test', job_require_num=10)
        Job.objects.create(id=3, project=_project, job_name='test_job',
                           job_worktime=5.0, job_content='content_test', job_require_num=10)
    # 发起签到

    def test_create_signproject(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'test1234', 'password': 'test1234'})
        assert response.status_code == 200

        response = client.post('/api/sign/project', {
            "title": "签到标题",
            "content": "签到内容",
            "begin_time": "2019-12-01 12:00:00",
            "end_time": "2019-12-01 13:00:00",
            "project": 1,
            "jobs": [3, 2],
            "position": "清华学堂",
            "longitude": 116.320002393781,
            "latitude": 40.0011853
        })
        assert response.status_code == 200

        response = client.post('/api/sign/project', {
            "title": "签到标题",
            "content": "签到内容",
            "begin_time": "2019-12-01 12:00:00",
            "end_time": "2019-12-01 13:00:00",
            "project": 1,
            "jobs": [3, 1]
        })
        assert response.status_code == 400

    # 查看签到项目

    # 测试函数执行后执行
    def tearDown(self):
        get_redis_connection("default").flushall()


class signinTestCase(TestCase):
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111, name='清小华', department='软件学院',
                       email='lixiaojia@163.com', phone=12233, id_card='11111119990000000X')
        _user.save()
        _project = Project(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req', begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0),
                           end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59), deadline=datetime.datetime(2035, 12, 1, 23, 59, 59))
        _project.save()
        _job = Job(id=1, project=_project, job_name='test_job',
                   job_worktime=5.0, job_content='content_test', job_require_num=10)
        _job.save()

        _join_record = JoinRecord.objects.create(user=_user, project=_project)
        _join_record.job.add(_job)
        _sign_project = SignProject.objects.create(project=_project, title='第一次活动', content='content', begin_time="2019-12-01 12:00:00", end_time="2035-12-01 12:00:00",
                                                   position="清华学堂", longitude=116.320002393781, latitude=40.0011853)
        _sign_project.jobs.add(_job)

    # 签到
    def test_signin(self):
        client = APIClient()
        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.post('/api/sign/signin', {'sign_project_id': 1,
                                                'longitude': 116.320002393781,
                                                'latitude': 40.0011853})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()


class signoutTestCase(TestCase):
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111, name='清小华', department='软件学院',
                       email='lixiaojia@163.com', phone=12233, id_card='11111119990000000X')
        _user.save()
        _project = Project(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req', begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0),
                           end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59), deadline=datetime.datetime(2035, 12, 1, 23, 59, 59))
        _project.save()
        _job = Job(id=1, project=_project, job_name='test_job',
                   job_worktime=5.0, job_content='content_test', job_require_num=10)
        _job.save()

        _join_record = JoinRecord.objects.create(user=_user, project=_project)
        _join_record.job.add(_job)
        _join_record.save()
        _sign_project = SignProject.objects.create(project=_project, title='第一次活动', content='content', begin_time=timezone.now() + datetime.timedelta(minutes=1), end_time=timezone.now(),
                                                   position="清华学堂", longitude=116.320002393781, latitude=40.0011853)
        _sign_project.jobs.add(_job)
        _sign_project.save()

        SignRecord.objects.create(
            id=1, join_record=_join_record, sign_project=_sign_project)
    # 签退

    def test_signout(self):
        client = APIClient()
        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.post('/api/sign/signout', {'sign_record_id': 1})
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()


class webuserTestCase(TestCase):
    def setUp(self):
        _webuser = WebUser.objects.create_superuser(id=1, username='admin', password='admin', email='xxx@mails.tsinghua.edu.cn')
        _webuser_1 = WebUser.objects.create_superuser(id=2, username='test_user', password='test_user', email='xxx@mails.tsinghua.edu.cn')

    def test_create_webuser(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200

        response = client.post('/api/auth/webuser', {'username': 'redcross',
                                                 'password': 'redcross',
                                                 'name': '清华大学红十字会',
                                                 'description': '这是简介',
                                                 'manager':'这是负责人',
                                                 'email':'xxx@mails.tsinghua.edu.cn',
                                                 'phone':13888888888
                                                 })
        assert response.status_code == 200

    def test_modify_webuser(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200

        response = client.put('/api/auth/webuser', {
            'name': '校团委管理员'
        })
        assert response.status_code == 200

        response = client.put('/api/auth/webuser?id=2', {
            'name': '测试管理员'
        })
        assert response.status_code == 200

    def test_get_webuser(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'test_user', 'password': 'test_user'})
        assert response.status_code == 200

        response = client.get('/api/auth/webuser')
        assert response.status_code == 200

        response = client.get('/api/auth/webuser?id=1')
        assert response.status_code == 200

    def test_delete_webuser(self):
        client = APIClient()
        response = client.post(
            '/api/auth/weblogin', {'username': 'admin', 'password': 'admin'})
        assert response.status_code == 200

        response = client.delete('/api/auth/webuser?id=2')
        assert response.status_code == 200

    def tearDown(self):
        get_redis_connection("default").flushall()

class commentTestCase(TestCase):
    def setUp(self):
        _webuser = WebUser.objects.create_user('test1234', password='test1234')
        # 在ApplyRecord中创建一条记录
        _user = WxUser(id=2017011111, name='清小华', department='软件学院',
                       email='lixiaojia@163.com', phone=12233)
        _user.save()
        _project = Project(id=1, webuser=_webuser, title='test', content='testcontent', introduction='intro', requirements='req', begin_datetime=datetime.datetime(2019, 12, 4, 0, 0, 0),
                           end_datetime=datetime.datetime(2035, 12, 5, 23, 59, 59), deadline=datetime.datetime(2035, 12, 1, 23, 59, 59))
        _project.save()
        _job = Job(id=1, project=_project, job_name='test_job',
                   job_worktime=5.0, job_content='content_test', job_require_num=10)
        _job.save()

        _join_record = JoinRecord.objects.create(user=_user, project=_project)
        _join_record.job.add(_job)
        _join_record.save()
    
    def test_comment(self):
        client = APIClient()
        response = client.post('/api/auth/login', {'token': 'null'})
        assert response.status_code == 200

        response = client.post('/api/my/comment', {"join_record_id":1,
                                                "comment":"评价",
                                                "comment_rank":5
                                                 })
        assert response.status_code == 200

        response = client.post('/api/my/comment', {"join_record_id":1,
                                                "comment":"评价",
                                                "comment_rank":5
                                                 })
        assert response.status_code == 406

        response = client.post('/api/my/comment', {"join_record_id":2,
                                                "comment":"评价",
                                                "comment_rank":5
                                                 })
        assert response.status_code == 404



    def tearDown(self):
        get_redis_connection("default").flushall()