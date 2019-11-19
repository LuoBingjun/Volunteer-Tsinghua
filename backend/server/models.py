from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class WxUser(models.Model):
    id = models.DecimalField('学生证号/工作证号', primary_key=True, max_digits=10, decimal_places=0)
    name = models.CharField('姓名', max_length=32)
    department = models.CharField('单位', max_length=32)
    email = models.EmailField('邮箱')
    phone = models.DecimalField('电话', null=True, blank=True, max_digits=11, decimal_places=0)
    openid = models.CharField('OpenID', null=True, blank=True, unique=True, max_length=64)
    join_time = models.DateTimeField('创建时间', auto_now_add=True)

class WebUser(AbstractUser):
    description = models.CharField('描述', blank=True, null=True, max_length=128)

class ApplyRecord(models.Model):
    user = models.ForeignKey('WxUser', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    form = models.TextField('报名表单')
    submit_time = models.DateTimeField('提交时间',auto_now_add=True)
    status = models.CharField('审核状态', max_length=1, default='W', choices=[('W', '待审核'), ('P', '审核通过'), ('N', '审核不通过')])
    # checked = models.BooleanField('审核状态', default=False)

class JoinRecord(models.Model):
    user = models.ForeignKey('WxUser', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    work_time = models.FloatField('工时', blank=True, null=True)
    sign_record = models.ManyToManyField('SignRecord', blank=True)

# 项目签到
class SignProject(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=128)
    content = models.TextField('详情')
    begin_time = models.DateTimeField('签到开始时间')
    end_time = models.DateTimeField('签到结束时间')
    # position = models.CharField(max_length=10)
    

class SignRecord(models.Model):
    join_record = models.ForeignKey('JoinRecord', on_delete=models.CASCADE)
    sign_project = models.ForeignKey('SignProject', on_delete=models.CASCADE)
    sign_in_time = models.DateTimeField('签到时间', auto_now_add=True)
    sign_out_time = models.DateTimeField('签退时间', blank=True, null=True)


class Project(models.Model):
    title = models.CharField('项目', max_length=128)
    content = models.TextField('详情')
    cover = models.ImageField('封面图片', blank=True)
    # require_num = models.PositiveIntegerField('需求人数')# 删掉
    requirements = models.TextField('需求')
    form = models.TextField('报名表单', blank=True)
    time = models.DateTimeField('创建时间', auto_now_add=True)
    deadline = models.DateTimeField('报名截止时间')
    finished = models.BooleanField('结项状态', default=False)

class Job(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    job_name = models.CharField('岗位', max_length=128)
    job_worktime = models.FloatField('工时')
    job_content = models.TextField('详情')
    job_require_num = models.PositiveIntegerField('需求人数')
