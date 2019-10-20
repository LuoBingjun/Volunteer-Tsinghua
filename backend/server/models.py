from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class User(models.Model):
    id = models.DecimalField('学生证号/工作证号', primary_key=True, max_digits=10, decimal_places=0)
    name = models.CharField('姓名', max_length=32)
    department = models.CharField('单位/班级', max_length=32)
    email = models.EmailField('邮箱')
    phone = models.DecimalField('电话', max_digits=11, decimal_places=0)
    join_time = models.DateTimeField('创建时间')

class AapplyRecord(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    form = JSONField('报名表单')
    submit_time = models.DateTimeField('提交时间')
    checked = models.BooleanField('审核状态')

class Project(models.Model):
    title = models.CharField('项目', max_length=128)
    content = models.TextField('详情')
    cover = models.ImageField('封面图片')
    require_num = models.PositiveIntegerField('需求人数')
    form = JSONField('报名表单')
    time = models.DateTimeField('创建时间')
    deadline = models.DateTimeField('截止日期')