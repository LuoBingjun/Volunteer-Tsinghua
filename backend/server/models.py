from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class WxUser(models.Model):
    id = models.DecimalField('学生证号/工作证号', primary_key=True, max_digits=10, decimal_places=0)
    name = models.CharField('姓名', max_length=32)
    department = models.CharField('单位', max_length=32)
    email = models.EmailField('邮箱')
    phone = models.DecimalField('电话', max_digits=11, decimal_places=0)
    id_card = models.CharField('身份证号', max_length=64)
    openid = models.CharField('OpenID', null=True, blank=True, unique=True, max_length=64)
    join_time = models.DateTimeField('创建时间', auto_now_add=True)

class WebUser(AbstractUser):
    name = models.CharField('组织名称', max_length=128)
    description = models.CharField('简介',blank=True, null=True, max_length=256)
    manager = models.CharField('负责人', blank=True, null=True, max_length=16)
    email = models.EmailField('电子邮箱', blank=True, null=True)
    phone = models.DecimalField('电话', null=True, blank=True, max_digits=11, decimal_places=0)
    head = models.ImageField('头像')

class ApplyRecord(models.Model):
    user = models.ForeignKey('WxUser', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    form = models.TextField('报名表单')
    submit_time = models.DateTimeField('提交时间',auto_now_add=True)
    status = models.CharField('审核状态', max_length=1, default='W', choices=[('W', '待审核'), ('P', '审核通过'), ('N', '审核不通过')])
    # checked = models.BooleanField('审核状态', default=False)

class JoinRecord(models.Model):
    user = models.ForeignKey('WxUser', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    job = models.ManyToManyField('Job')
    work_time = models.FloatField('工时', blank=True, null=True)
    comment_rank = models.IntegerField('评分', blank=True, null=True)
    comment = models.TextField('评价', blank=True, null=True)
    is_comment = models.BooleanField('评价状态', default=False)

# 项目签到
class SignProject(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=128)
    content = models.TextField('详情')
    begin_time = models.DateTimeField('签到开始时间')
    end_time = models.DateTimeField('签到结束时间')
    jobs = models.ManyToManyField('Job')
    position = models.CharField(max_length=32)
    longitude = models.FloatField('经度')
    latitude = models.FloatField('纬度')
    

class SignRecord(models.Model):
    join_record = models.ForeignKey('JoinRecord', on_delete=models.CASCADE)
    sign_project = models.ForeignKey('SignProject', on_delete=models.CASCADE)
    sign_in_time = models.DateTimeField('签到时间', auto_now_add=True)
    sign_out_time = models.DateTimeField('签退时间', blank=True, null=True)


class Project(models.Model):
    webuser = models.ForeignKey('WebUser', on_delete=models.CASCADE)
    title = models.CharField('项目', max_length=128)
    introduction = models.CharField('简介', max_length=32)
    content = models.TextField('详情')
    type = models.CharField('种类', max_length=2, choices=[('WH','文化教育'),('SH', '赛会服务'), ('SQ', '社区服务'), ('YL', '医疗卫生'), ('JK', '健康残障'), ('XY', '校园讲解'), ('QT', '其他')])
    cover = models.ImageField('封面图片', blank=True)
    requirements = models.TextField('需求')
    form = models.TextField('报名表单', blank=True)
    time = models.DateTimeField('创建时间', auto_now_add=True)
    qrcode_1 = models.ImageField('二维码1', blank=True, null=True)
    qrcode_2 = models.ImageField('二维码2', blank=True, null=True)
    success_note = models.TextField('成功提示', blank=True, null=True)
    deadline = models.DateTimeField('报名截止时间')
    begin_datetime = models.DateTimeField('项目开始时间')
    end_datetime = models.DateTimeField('项目结束时间')
    finished = models.BooleanField('结项状态', default=False)

class Message(models.Model):
    type = models.CharField('消息类型', choices=[('M', '模板消息'), ('P', '普通消息')], max_length=1)
    sender = models.ForeignKey('WebUser', on_delete=models.CASCADE)
    receiver = models.ForeignKey('WxUser', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    title = models.CharField('标题', null=True, blank=True, max_length=24)
    content = models.TextField('内容', null=True, blank=True)


class Job(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    job_name = models.CharField('岗位', max_length=128)
    job_worktime = models.FloatField('工时')
    job_content = models.TextField('详情')
    job_require_num = models.PositiveIntegerField('需求人数')
